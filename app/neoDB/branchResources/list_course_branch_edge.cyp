MATCH
    (branch:Branch),
    (user:User{userId: $userId})
WITH 
    branch,
    user,
    EXISTS((user)-[:PRIVILEGED_OF]->(:Permission{role:'DLTC'})) as isDLTC,
    EXISTS((user)-[:PRIVILEGED_OF]->(:Permission{role:'DLTC'})) as isInstructor,
    EXISTS((user)-[:USER_TEACH]->()-[:COURSE_DESCRIBE]->(:GraphConcept{name: $courseCode})) as isAssigned
WHERE
    branch.deltaGraphId CONTAINS replace($courseCode,' ' ,'_') AND (
        (branch.visibility = 'public') OR
        (branch.visibility = 'colleague' AND (isDLTC OR isInstructor)) OR
        (branch.visibility = 'instructor' AND isInstructor) OR
        (branch.visibility = 'collaborator' AND isAssigned) OR
        EXISTS((branch)<-[:USER_OWN]-(user))
    )
WITH DISTINCT branch
MATCH
    (branch)-[edges_a:PATCH|FORK|TRUNK_PULL|BRANCH_PULL]->(),
    ()-[edges_b:PATCH|FORK|TRUNK_PULL|BRANCH_PULL]->(branch)
WITH collect(edges_a)+collect(edges_b) as edges_list
UNWIND edges_list as edges
WITH DISTINCT edges
RETURN edges
