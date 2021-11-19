MATCH (branch:Branch{deltaGraphId: $deltaGraphId})<-[:USER_OWN]-(user:User{userId: $userId})
SET branch.isExposed = $isExposed
RETURN branch