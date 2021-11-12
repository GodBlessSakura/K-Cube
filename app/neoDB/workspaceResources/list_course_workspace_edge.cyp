MATCH
    (workspace:Workspace)<-[:USER_OWN]-(user:User{userId: $userId})
WHERE
    split(workspace.deltaGraphId,'.')[0] = replace($courseCode,' ' ,'_')
WITH DISTINCT workspace
MATCH
    (workspace)-[edges:WORK_ON]->()
RETURN DISTINCT edges
