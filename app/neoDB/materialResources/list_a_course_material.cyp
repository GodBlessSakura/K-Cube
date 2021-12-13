MATCH (course:Course)-[:COURSE_DESCRIBE]->(courseConcept{name: $courseCode})
MATCH (concept:GraphConcept)<-[:CONTENT_DESCRIBE]-(material:Material{courseNodeId: id(course)})<-[:INSTRUCTOR_CREATE]-(user:User)
WHERE  EXISTS((user)-[:USER_TEACH]->()-[:COURSE_DESCRIBE]->(:GraphConcept{name: $courseCode}))
RETURN material, concept, user