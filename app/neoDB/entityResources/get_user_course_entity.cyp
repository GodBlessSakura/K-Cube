MATCH (course:Course)-[:COURSE_DESCRIBE]->(courseConcept{name: $courseCode}),(concept:GraphConcept{name: $name})
OPTIONAL MATCH (concept)-[:CONTENT_DESCRIBE|ACTIVITY_OF]-(data{courseNodeId: id(course)})<-[:INSTRUCTOR_CREATE]-(:User{userId: $userId})
RETURN DISTINCT concept, collect(data) as data