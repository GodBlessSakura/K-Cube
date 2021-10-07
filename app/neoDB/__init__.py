from neo4j import GraphDatabase
from .user import userResources
from neo4j import GraphDatabase
class allResources(userResources):
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.user = userResources(self.driver)

    def close(self):
        self.driver.close()
