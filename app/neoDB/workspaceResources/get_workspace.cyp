MATCH (owner:User{userId: $userId})
WITH DISTINCT owner
MATCH (workspace:Workspace{deltaGraphId: $deltaGraphId})<-[:USER_OWN]-(owner)
RETURN workspace