MATCH (course:Course)-[:COURSE_DESCRIBE]->(courseConcept{name: $courseCode})
MATCH (concept:GraphConcept)<-[:CONTENT_DESCRIBE]-(material:Material{courseNodeId: id(course)})<-[:INSTRUCTOR_CREATE]-(:User{userId: $userId})
RETURN material, concept