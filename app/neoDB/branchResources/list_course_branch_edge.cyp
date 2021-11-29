MATCH
    (branch:Branch),
    (user:User{userId: $userId}),
    (course:Course)-[:COURSE_DESCRIBE]->(courseConcept{name: $courseCode})
WITH 
    branch,
    user,
    EXISTS((user)-[:PRIVILEGED_OF]->(:Permission{role:'DLTC'})) as isDLTC,
    EXISTS((user)-[:PRIVILEGED_OF]->(:Permission{role:'instructor'})) as isInstructor,
    EXISTS((user)-[:USER_TEACH]->()-[:COURSE_DESCRIBE]->(:GraphConcept{name: $courseCode})) as isAssigned
WHERE
    split(branch.deltaGraphId,'.')[0] = toString(id(course)) AND (
        (branch.visibility = 4) OR
        (branch.visibility = 3 AND (isDLTC OR isInstructor)) OR
        (branch.visibility = 2 AND isInstructor) OR
        (branch.visibility = 1 AND isAssigned) OR
        EXISTS((branch)<-[:USER_OWN]-(user))
    )
WITH DISTINCT branch
CALL{
    WITH branch
    MATCH (branch)-[edges:PATCH|FORK|TRUNK_PULL|BRANCH_PULL]->()
    RETURN edges
UNION
    WITH branch
    MATCH ()-[edges:PATCH|FORK|TRUNK_PULL|BRANCH_PULL]->(branch)
    RETURN edges
}
RETURN DISTINCT edges
