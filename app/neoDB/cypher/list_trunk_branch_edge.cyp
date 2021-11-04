MATCH
    (trunk:Trunk),
    (branch:Branch)
WITH collect(trunk, branch) AS nodes
WHERE nodes.deltaGraphId CONTAINS replace($courseCode,' ' ,'_')
UNWIND nodes AS n
UNWIND nodes AS m
MATCH
    (n)-[edges:OVERWRITE]->(m)
RETURN edges
