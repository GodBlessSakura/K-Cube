MATCH (course:Course)-[:COURSE_DESCRIBE]->(courseConcept),(user{userId: $userId})-[:PRIVILEGED_OF]->(:Permission{canViewInternalCourse:true})
WITH distinct user, course, courseConcept
RETURN course, courseConcept, EXISTS((user)-[:USER_TEACH]->(course)) as isTeaching