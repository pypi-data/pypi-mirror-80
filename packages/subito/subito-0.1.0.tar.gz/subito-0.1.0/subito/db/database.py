import logging
from os import getenv

from tinydb import TinyDB


class Database:
    """ Class for handling local service information and storing queues """

    def __init__(self, *args):
        """ Accepts any number of strings based on which to create or connect databases """
        self.dbs = {arg: TinyDB(f"{arg}.json") for arg in args}
        self.logger = logging.getLogger("__main__")
        self.logger.setLevel(getenv("LEVEL"))

    def get_id(self, document):
        """ Returns document ID """
        return document.doc_id if hasattr(document, "doc_id") else None

    def remove(self, db, ID):
        """ Removes a document from a db by ID """
        self.dbs[db].remove(doc_ids=[ID])
        self.logger.info(f"Removed document from {db} with id {ID}")

    def insert(self, db, document):
        """ Inserts document and returns it's ID if not already inserted """
        ID = self.get_id(document)
        if ID is None:
            ID = self.dbs[db].insert(document)
            self.logger.info(f"Inserted document to {db} with id {ID}")

        return ID

    def documents(self, db):
        """ Returns all documents from db """
        documents = self.dbs[db].all()
        return documents
