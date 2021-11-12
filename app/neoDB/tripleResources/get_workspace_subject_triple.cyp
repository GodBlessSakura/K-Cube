MATCH (owner:User{userId: $userId})
WITH DISTINCT owner
MATCH (owner)-[:USER_OWN]->(workspace:Workspace{deltaGraphId: $deltaGraphId})-[:WORK_ON]->(subject)
WITH DISTINCT subject
MATCH (h:GraphConcept)-[r:DELTA_GRAPH_RELATIONSHIP{deltaGraphId: subject.deltaGraphId}]->(t:GraphConcept)
RETURN h.name, r.name, t.name, r.value