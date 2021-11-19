MATCH (course:GraphConcept{name: $courseCode})-[:COURSE_DESCRIBE]-()<-[:TRUNK_DESCRIBE]-(trunk)
WITH course
CALL{
    WITH course
    MATCH (course)-[:COURSE_DESCRIBE]-()<-[:TRUNK_DESCRIBE]-(trunk)
    WITH DISTINCT trunk
    MATCH (h:GraphConcept)-[r:DELTA_GRAPH_RELATIONSHIP{deltaGraphId: trunk.deltaGraphId}]->(t:GraphConcept)
    RETURN h.name as h_name, r.name as r_name, t.name as t_name, r.value as r_value
UNION
    WITH course
    MATCH (branch:Branch{isExposed: true})
    WHERE split(branch.deltaGraphId,'.')[0] = replace($courseCode,' ' ,'_')
    WITH DISTINCT branch
    MATCH (h:GraphConcept)-[r:DELTA_GRAPH_RELATIONSHIP{deltaGraphId: branch.deltaGraphId}]->(t:GraphConcept)
    RETURN h.name as h_name, r.name as r_name, t.name as t_name, r.value as r_value
}
RETURN h_name, r_name, t_name, r_value, count(*) as count