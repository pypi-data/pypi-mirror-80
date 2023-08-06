from asyncio import gather

from gql import Client, WebsocketsTransport

from subito.operations.subscription import Subscription
from subito.operations.operation import Operation


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
            await gather(*(s.consume(session) for s in Subito.subscriptions))

    @staticmethod
    def subscribe(document: str):
        Subito.subscriptions.append(Subscription(document))

        def inner(handler):
            subscription = Subito.subscriptions[-1]
            subscription.handler = handler

        return inner

    @staticmethod
    async def execute(document: str, variables: dict = {}) -> dict:
        operation = Operation(document, variables)
        result = await operation.execute(Subito.session)
        return result