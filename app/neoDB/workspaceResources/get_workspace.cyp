MATCH (owner:User{userId: $userId})
WITH DISTINCT owner
MATCH
    (workspace:Workspace{deltaGraphId: $deltaGraphId})<-[:USER_OWN]-(owner),
    (course:Course)
WHERE toString(id(course)) = split($deltaGraphId,'.')[0]
RETURN workspace, course, EXISTS((course)<-[:BRANCH_DESCRIBE]-(workspace)) as isExposed