MATCH
    (branch:Branch),
    (user:User{userId: $userId})
WITH 
    branch,
    user,
    EXISTS((user)-[:PRIVILEGED_OF]->(:Permission{role:'DLTC'})) as isDLTC,
    EXISTS((user)-[:PRIVILEGED_OF]->(:Permission{role:'instructor'})) as isInstructor,
    EXISTS((user)-[:USER_TEACH]->()-[:COURSE_DESCRIBE]->(:GraphConcept{name: $courseCode})) as isAssigned,
    EXISTS((branch)<-[:USER_OWN]-(user)) as isOwner
WHERE
    split(branch.deltaGraphId,'.')[0] = replace($courseCode,' ' ,'_') AND (
        (branch.visibility = 4) OR
        (branch.visibility = 3 AND (isDLTC OR isInstructor)) OR
        (branch.visibility = 2 AND isInstructor) OR
        (branch.visibility = 1 AND isAssigned) OR
        isOwner
    )
RETURN DISTINCT branch AS nodes, isOwner
