MATCH (workspace:Workspace)<-[:USER_OWN]-(user:User{userId: $userId})
WHERE split(workspace.deltaGraphId,'.')[0] = replace($courseCode,' ' ,'_')
RETURN DISTINCT workspace AS nodes, EXISTS((user)-[:USER_OWN]->(:Branch)<-[:WORK_ON]-(workspace)) AS canPatch
