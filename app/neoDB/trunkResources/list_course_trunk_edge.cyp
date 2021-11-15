MATCH
    (nodes:Trunk)
WHERE split(nodes.deltaGraphId,'.')[0] = replace($courseCode,' ' ,'_')
WITH DISTINCT nodes
CALL{
    WITH nodes
    MATCH (nodes)-[edges:PATCH|FORK]->(:Trunk)
    RETURN edges
UNION
    WITH nodes
    MATCH (:Trunk)-[edges:PATCH|FORK]->(nodes)
    RETURN edges
}
RETURN DISTINCT edges as edges
