MATCH
    (nodes:Trunk)
WHERE nodes.deltaGraphId CONTAINS replace($courseCode,' ' ,'_')
UNWIND nodes AS n
UNWIND nodes AS m
MATCH
    (n)-[edges:PATCH|FORK]->(m)
RETURN DISTINCT edges as edges
