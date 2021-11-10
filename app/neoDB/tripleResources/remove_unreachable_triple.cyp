MATCH (workspace:Workspace{deltaGraphId: $deltaGraphId})<-[:USER_OWN]-(:User{userId: $userId})
WITH DISTINCT workspace
MATCH (root:GraphConcept{name: split($deltaGraphId,'.')[0]})
WITH workspace, root
OPTIONAL MATCH reachable=(root)-[:DELTA_GRAPH_RELATIONSHIP*{deltaGraphId : workspace.deltaGraphId}]-(:GraphConcept)
UNWIND (
    CASE reachable
        WHEN null THEN [null]
        ELSE relationships(reachable)
    END) AS reachable_relationships
WITH collect(id(reachable_relationships)) AS reachable_id, workspace
MATCH (h)-[r:DELTA_GRAPH_RELATIONSHIP{deltaGraphId : workspace.deltaGraphId}]->(t)
WHERE NOT id(r) IN reachable_id
WITH collect(h.name) AS h_name, collect(r.name) AS r_name, collect(t.name) AS t_name, r, workspace
DELETE r
SET workspace.lAStModified = datetime.transaction()
RETURN h_name, r_name, t_name;