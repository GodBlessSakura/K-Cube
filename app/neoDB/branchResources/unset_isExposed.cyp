MATCH (branch:Branch{deltaGraphId: $deltaGraphId})<-[:USER_OWN]-(user:User{userId: $userId})
WITH branch
MATCH(course:Course)
WHERE toString(id(course)) = split($deltaGraphId,'.')[0]
WITH branch, course
MATCH (course)<-[wasExposed:BRANCH_DESCRIBE{userId: $userId}]-(branch)
DELETE wasExposed
RETURN branch