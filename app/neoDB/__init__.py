from neo4j import GraphDatabase
from .user import userResources
from neo4j import GraphDatabase


class APIDriver(userResources):
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)
        self.user = userResources(self)

    def close(self):
        self.driver.close()
