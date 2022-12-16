MATCH (owner:User{userId: $userId})
WITH DISTINCT owner
MATCH
    (workspace:Workspace{deltaGraphId: $deltaGraphId})<-[:USER_OWN]-(owner),
    (workspace)-[:WORK_ON]->(subject),
    (course)-[:COURSE_DESCRIBE]->(courseConcept)
OPTIONAL MATCH (subject)-[:PATCH|FORK]->(predecessor)
WHERE toString(id(course)) = split($deltaGraphId,'.')[0]
RETURN subject, NOT EXISTS((subject)<-[:PATCH]-()) as isPatchLeaf, EXISTS((subject)<-[:USER_OWN]-(owner)) as isOwner, courseConcept.name as courseCode, EXISTS((course)<-[:BRANCH_DESCRIBE]-(subject)) as isExposed, EXISTS((owner)-[:USER_TEACH]->(course)) as isTeaching, predecessor.deltaGraphId as predecessor