import asyncio

from subito.operations import operation


class Subscription(operation.Operation):
    def __init__(self, document: str):
        """ Initiates a subscription monitor. \nIt accepts a document argument which represents a path to a file or a string representing graphql subscription and a handler function to process messages """
        super().__init__(document)
        self._handler = None

    async def consume(self, session):
        """ Subscribe to a subscription, and process it's messages """
        async for message in session.subscribe(self.ast):
            await self.process(message)

    async def process(self, data):
        """ Send to a service for further processing """
        return await self.handler(data)

    @property
    def handler(self):
        return self._handler

    @handler.setter
    def handler(self, handler):
        self._handler = handler
