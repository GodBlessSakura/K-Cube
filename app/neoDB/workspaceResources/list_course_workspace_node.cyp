MATCH
    (workspace:Workspace)<-[:USER_OWN]-(user:User{userId: $userId})
WHERE
    workspace.deltaGraphId CONTAINS replace($courseCode,' ' ,'_')
RETURN DISTINCT workspace AS nodes