MATCH (workspace:Workspace{deltaGraphId: $deltaGraphId})<-[:USER_OWN]-(:User{userId: $userId})
WITH DISTINCT workspace
MATCH (root:GraphConcept{name: split($deltaGraphId,'.')[0]})
WITH workspace, root
MATCH reachable=(root)-[:DELTA_GRAPH_RELATIONSHIP*{deltaGraphId : workspace.deltaGraphId}]-(:GraphConcept)
UNWIND relationships(reachable) AS reachable_relationships
WITH collect(id(reachable_relationships)) as reachable_id, workspace
MATCH (h)-[r:DELTA_GRAPH_RELATIONSHIP{deltaGraphId : workspace.deltaGraphId}]->(t)
WHERE NOT id(r) IN reachable_id
WITH collect(h.name) as h_name, collect(r.name) as r_name, collect(t.name) as t_name, r, workspace
DELETE r
SET workspace.lastModified = datetime.transaction()
RETURN h_name, r_name, t_name;