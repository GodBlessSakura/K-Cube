MATCH (owner:User{userId: $userId})
WITH DISTINCT owner
MATCH
    (workspace:Workspace{deltaGraphId: $deltaGraphId})<-[:USER_OWN]-(owner),
    (:GraphConcept{name: split($deltaGraphId,'.')[0]})<-[:COURSE_DESCRIBE]-(course)
RETURN workspace, course