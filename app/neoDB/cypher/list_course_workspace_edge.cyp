MATCH
    (workspace:Workspace)<-[:USER_OWN]-(user:User{userId: $userId})
WHERE
    workspace.deltaGraphId CONTAINS replace($courseCode,' ' ,'_')
WITH DISTINCT workspace
MATCH
    (workspace)-[edges:WORK_ON]->(),
RETURN DISTINCT edges
