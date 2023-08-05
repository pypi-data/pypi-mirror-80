from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from future import standard_library
standard_library.install_aliases()
from builtins import object
from gcloud.rest.auth import BUILD_GCLOUD_REST  # pylint: disable=no-name-in-module

if BUILD_GCLOUD_REST:
    class FlowControl(object):
        def __init__(self, **kwargs)        :
            raise NotImplementedError('this class is only implemented in aio')

    class SubscriberClient(object):
        def __init__(self, **kwargs)        :
            raise NotImplementedError('this class is only implemented in aio')

else:
    import asyncio
    import concurrent.futures
    import signal
    from typing import Any
    from typing import Callable
    from typing import Dict
    from typing import List
    from typing import Optional
    from typing import Tuple
    from typing import Union

    from google.api_core import exceptions
    from google.cloud import pubsub
    from google.cloud.pubsub_v1.types import FlowControl as _FlowControl
    from google.cloud.pubsub_v1.subscriber.message import Message

    from .subscriber_message import SubscriberMessage
    from .utils import convert_google_future_to_concurrent_future


    class FlowControl(object):
        def __init__(self, *args           , **kwargs                )        :
            """
            FlowControl transitional wrapper.
            (FlowControl fields docs)[https://github.com/googleapis/python-pubsub/blob/6b9eec81ccee81ab93646eaf7652139fc218ed36/google/cloud/pubsub_v1/types.py#L139-L159]  # pylint: disable=line-too-long
            Google uses a named tuple; here are the fields, defaults:
            - max_bytes: int = 100 * 1024 * 1024
            - max_messages: int = 1000
            - max_lease_duration: int = 1 * 60 * 60
            - max_duration_per_lease_extension: int = 0
            """
            self._flow_control = _FlowControl(*args, **kwargs)

        def __getitem__(self, index     )       :
            return self._flow_control[index]


    class SubscriberClient(object):
        def __init__(self,
                     **kwargs                )        :
            if 'loop' in kwargs: loop = kwargs['loop']; del kwargs['loop']
            else: loop =  None
            self._subscriber = pubsub.SubscriberClient(**kwargs)
            self.loop = loop or asyncio.get_event_loop()

        def create_subscription(self,
                                subscription     ,
                                topic     ,
                                **kwargs                
                                )        :
            """
            Create subscription if it does not exist. Check out the official
            [create_subscription docs](https://github.com/googleapis/google-cloud-python/blob/11c72ade8b282ae1917fba19e7f4e0fe7176d12b/pubsub/google/cloud/pubsub_v1/gapic/subscriber_client.py#L236)  # pylint: disable=line-too-long
            for more details
            """
            try:
                self._subscriber.create_subscription(
                    subscription,
                    topic,
                    **kwargs
                )
            except exceptions.AlreadyExists:
                pass

        def subscribe(self,
                      subscription     ,
                      callback                                    , **_3to2kwargs
                      )                  :  # type: ignore
            if 'flow_control' in _3to2kwargs: flow_control = _3to2kwargs['flow_control']; del _3to2kwargs['flow_control']
            else: flow_control =  ()
            """
            Create subscription through pubsub client, hijack the returned
            "non-concurrent Future" and coerce it into being a "concurrent
            Future", wrap it into a asyncio Future and return it.
            """
            sub_keepalive                 = (  # type: ignore
                self._subscriber.subscribe(
                    subscription,
                    self._wrap_callback(callback),
                    flow_control=flow_control))

            convert_google_future_to_concurrent_future(
                sub_keepalive, loop=self.loop)

            _ = asyncio.wrap_future(sub_keepalive)
            self.loop.add_signal_handler(signal.SIGTERM, sub_keepalive.cancel)

            return sub_keepalive

        def run_forever(self,
                        sub_keepalive                )        :  # type: ignore
            """
            Start the asyncio loop, running until it is either SIGTERM-ed or
            killed by keyboard interrupt. The Future parameter is used to
            cancel subscription Future in the case that an unexpected exception
            is thrown. You can also directly pass the `.subscribe()` method
            call instead like so:
                sub.run_forever(sub.subscribe(callback))
            """
            try:
                self.loop.run_forever()
            except (KeyboardInterrupt, concurrent.futures.CancelledError):
                pass
            finally:
                # 1. stop the `SubscriberClient` future, which will prevent
                #    more tasks from being leased
                if not sub_keepalive.cancelled():
                    sub_keepalive.cancel()
                # 2. cancel the tasks we already have, which should just be
                #    `worker` instances; note they have
                #    `except CancelledError: pass`
                for task in asyncio.Task.all_tasks(loop=self.loop):
                    task.cancel()
                # 3. stop the `asyncio` event loop
                self.loop.stop()

        def _wrap_callback(self,
                           callback                                     
                           )                             :
            """Schedule callback to be called from the event loop"""
            def _callback_wrapper(message         )        :
                asyncio.run_coroutine_threadsafe(
                    callback(  # type: ignore
                        SubscriberMessage.from_google_cloud(
                            message)),
                    self.loop)

            return _callback_wrapper
