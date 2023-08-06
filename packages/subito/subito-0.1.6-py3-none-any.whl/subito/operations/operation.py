import logging
from os.path import isfile

from gql import gql
from graphql import GraphQLSyntaxError, DocumentNode


class Operation:
    def __init__(self, document: str, variables: dict = {}):
        """ Defines an operation which parses and validates passed document """
        try:
            self.logger = logging.getLogger("__main__")
            self.document = document
            if isfile(self.document):
                with open(document) as f:
                    self.ast = gql(f.read())
            else:
                self.ast = gql(self.document)
            (self.definition,) = self.ast.definitions

            if self.definition.kind != "operation_definition":
                raise TypeError("document does not contain an an operation")

            self._variables = variables

        except GraphQLSyntaxError as e:
            raise TypeError("document has syntax errors")

    @property
    def name(self):
        """ Get operation name  """
        (selection,) = self.definition.selection_set.selections
        return selection.name.value

    async def execute(self, session):
        """ Send to a service for further processing """
        return await session.execute(self.ast, variable_values=self.variables)

    @property
    def variables(self):
        return self._variables

    @variables.setter
    def variables(self, variables):
        self._variables = variables