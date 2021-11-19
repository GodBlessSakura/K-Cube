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
        EXISTS((user)-[:USER_TEACH]->()-[:COURSE_DESCRIBE]->(:GraphConcept{name: split(graph.deltaGraphId,'.')[0]})) as isAssigned,
        EXISTS((graph)<-[:USER_OWN]-(user)) as isOwner
    WHERE        
        (graph.visibility = 4) OR
        (graph.visibility = 3 AND (isDLTC OR isInstructor)) OR
        (graph.visibility = 2 AND isInstructor) OR
        (graph.visibility = 1 AND isAssigned) OR
        isOwner
    RETURN graph, isOwner
UNION
    MATCH (graph:Trunk{deltaGraphId: $deltaGraphId})
    RETURN graph, false as isOwner
}
MATCH (:GraphConcept{name: split(graph.deltaGraphId,'.')[0]})<-[:COURSE_DESCRIBE]-(course)
RETURN DISTINCT graph, course, isOwner