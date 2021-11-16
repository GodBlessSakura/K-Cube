MATCH (:GraphConcept{name: $courseCode})-[:COURSE_DESCRIBE]-()<-[:TRUNK_DESCRIBE]-(trunk)
WITH DISTINCT trunk
MATCH (h:GraphConcept)-[r:DELTA_GRAPH_RELATIONSHIP{deltaGraphId: trunk.deltaGraphId}]->(t:GraphConcept)
RETURN h.name, r.name, t.name, r.value