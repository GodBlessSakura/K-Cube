MATCH (course:Course)-[:COURSE_DESCRIBE]->(courseConcept{name: $courseCode})
MATCH (concept:GraphConcept)<-[:ACTIVITY_OF]-(activity:Activity{courseNodeId: id(course)})<-[:INSTRUCTOR_CREATE]-(user:User{userId: $userId})
RETURN activity, concept, user