MATCH
    (nodes:Trunk)
WHERE split(nodes.deltaGraphId,'.')[0] = replace($courseCode,' ' ,'_')
UNWIND nodes AS n
UNWIND nodes AS m
MATCH
    (n)-[edges:PATCH|FORK|TRUNK_PULL|BRANCH_PULL]->(m)
RETURN DISTINCT edges as edges
