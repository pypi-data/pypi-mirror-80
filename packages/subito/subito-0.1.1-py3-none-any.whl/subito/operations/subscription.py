import asyncio
from types import FunctionType

from box import Box

from subito.db import queue
from subito.utils import extract
from subito.operations import operation


# TODO: Appropriate decorators inside class - how?
def exceptionHandler(decorated):
    async def wrapper(self, *args, **kwargs):
        try:
            await decorated(self, *args, **kwargs)
        except Exception as e:
            self.logger.error(f"Service not implemented or unavailable for {self.name}")

    return wrapper


def queueHandler(decorated):
    async def wrapper(self, *args, **kwargs):
        if not kwargs:
            return

        ID = self.queue.schedule(kwargs)
        result = await decorated(self, Box(kwargs))
        self.queue.complete(ID)
        return result

    return wrapper


class Subscription(operation.Operation):
    def __init__(self, document: str):
        """ Initiates a subscription monitor. \nIt accepts a document argument which represents a path to a file or a string representing graphql subscription and a handler function to process messages """
        super().__init__(document)
        self._handler = None
        self.queue = queue.Queue(self.name)

    @exceptionHandler
    async def dequeue(self, session):
        """ If messages queued in database process those """
        # async with self.client as session:
        if messages := self.queue.queue():
            await asyncio.gather(*[self.process(**message) for message in messages])

    @exceptionHandler
    async def subscribe(self, session):
        """ Subscribe to a subscription, and process it's messages """
        async for message in session.subscribe(self.ast):
            await self.process(**message)

    @queueHandler
    async def process(self, data):
        """ Send to a service for further processing """
        return await self.handler(data)

    @property
    def handler(self):
        return self._handler

    @handler.setter
    def handler(self, handler):
        self._handler = handler
