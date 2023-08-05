from subito.db import database


class Queue(database.Database):
    def __init__(self, subscription):
        """ Creates a database object for queing subscription messages """
        super().__init__(subscription)
        self.subscription = subscription

    def queue(self):
        return self.documents(self.subscription)

    def schedule(self, message):
        return self.insert(self.subscription, message)

    def complete(self, message):
        return self.remove(self.subscription, message)
