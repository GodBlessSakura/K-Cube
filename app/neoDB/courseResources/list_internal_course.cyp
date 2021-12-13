MATCH (course:Course)-[:COURSE_DESCRIBE]->(courseConcept)
RETURN course,courseConcept, EXISTS(({userId: $userId})-[:USER_TEACH]->(course)) as isTeaching