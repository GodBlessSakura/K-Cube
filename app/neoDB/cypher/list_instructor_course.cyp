MATCH ({userId: $userId})-[:USER_TEACH]->(course:Course)-[:COURSE_DESCRIBE]->(courseConcept)
RETURN course,courseConcept