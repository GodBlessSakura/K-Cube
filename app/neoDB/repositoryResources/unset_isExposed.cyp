MATCH (repo:Repository{deltaGraphId: $deltaGraphId})<-[:USER_OWN]-(user:User{userId: $userId})
WITH repo
MATCH (course:Course)
WHERE toString(id(course)) = split($deltaGraphId,'.')[0]
WITH repo, course
OPTIONAL MATCH (course)<-[wasExposed:REPO_DESCRIBE{userId: $userId}]-(:Repository)
DELETE wasExposed
RETURN branch