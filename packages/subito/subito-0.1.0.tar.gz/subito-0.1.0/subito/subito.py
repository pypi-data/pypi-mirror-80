from asyncio import gather
from types import FunctionType

from gql import Client, WebsocketsTransport

from subito.operations.subscription import Subscription


class Subito:
    session = None
    subscriptions = []

    def __init__(self, url: str):
        self.url = url
        self.options = {
            "transport": WebsocketsTransport(url=self.url),
            "fetch_schema_from_transport": True,
        }

    async def run(self):
        async with Client(**self.options) as session:
            Subito.session = session
            await gather(*(s.dequeue(session) for s in Subito.subscriptions))
            await gather(*(s.subscribe(session) for s in Subito.subscriptions))

    def subscribe(self, document: str):
        Subito.subscriptions.append(Subscription(document))

        def inner(handler):
            subscription = Subito.subscriptions[-1]
            subscription.handler = handler

            async def wrapper(self, *args, **kwargs):
                return handler

            return wrapper

        return inner
