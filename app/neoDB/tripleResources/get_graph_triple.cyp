MATCH (user:User{userId: $userId})
WITH user
CALL{
    WITH user
    MATCH (graph:Branch{deltaGraphId: $deltaGraphId})
    WITH 
        graph,
        user,
        EXISTS((user)-[:PRIVILEGED_OF]->(:Permission{role:'DLTC'})) as isDLTC,
        EXISTS((user)-[:PRIVILEGED_OF]->(:Permission{role:'instructor'})) as isInstructor,
        EXISTS((user)-[:USER_TEACH]->()-[:COURSE_DESCRIBE]->(:GraphConcept{name: split(graph.deltaGraphId,'.')[0]})) as isAssigned
    WHERE
        (graph.visibility = 'public') OR
        (graph.visibility = 'colleague' AND (isDLTC OR isInstructor)) OR
        (graph.visibility = 'instructor' AND isInstructor) OR
        (graph.visibility = 'collaborator' AND isAssigned) OR
        EXISTS((graph)<-[:USER_OWN]-(user))
        
    RETURN graph
UNION
    MATCH (graph:Trunk{deltaGraphId: $deltaGraphId})
    RETURN graph
}
WITH DISTINCT graph
MATCH (h:GraphConcept)-[r:DELTA_GRAPH_RELATIONSHIP{deltaGraphId: graph.deltaGraphId}]->(t:GraphConcept)
RETURN h.name, r.name, t.name, r.value