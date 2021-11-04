from neo4j.exceptions import ConstraintError
from .resourcesGuard import for_all_methods, reject_invalid
import sys
from .cypher import cypher


@for_all_methods(reject_invalid)
class workspaceResources:
    def __init__(self, driver):
        self.driver = driver
