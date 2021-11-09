MATCH (owner:User{userId: $userId})
WITH DISTINCT owner
MATCH
    (workspace:Workspace{deltaGraphId: $deltaGraphId})<-[:USER_OWN]-(owner),
    (workspace)-[:WORK_ON]->(subject)
RETURN subject, NOT EXISTS((subject)<-[:PATCH]-()) as isUpToDate