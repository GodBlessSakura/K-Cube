MATCH (owner:User{userId: $userId})
WITH DISTINCT owner
MATCH (workspace:Workspace{deltaGraphId: $deltaGraphId})<-[:USER_OWN]-(owner)
WITH DISTINCT workspace
MATCH (h:GraphConcept)-[r:DELTA_GRAPH_RELATIONSHIP{deltaGraphId: $deltaGraphId}]->(t:GraphConcept)
RETURN h.name, r.name, t.name, r.value