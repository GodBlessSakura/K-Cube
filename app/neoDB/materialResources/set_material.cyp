MATCH (course:Course)-[:COURSE_DESCRIBE]->(courseConcept{name: $courseCode})
MATCH (:GraphConcept{name: $name})<-[:CONTENT_DESCRIBE]-(material:Material{courseNodeId: id(course)})<-[:INSTRUCTOR_CREATE]-(:User{userId: $userId})
SET
    material.url = $url,
    material.desc = $desc
RETURN material, concept
