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
RETURN DISTINCT branch AS nodes
