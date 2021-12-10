MATCH (concept:GraphConcept)<-[:CONTENT_DESCRIBE]-(material:Material{courseCode: $courseCode})<-[:INSTRUCTOR_CREATE]-(user:User)
WHERE  EXISTS((user)-[:USER_TEACH]->()-[:COURSE_DESCRIBE]->(:GraphConcept{name: $courseCode}))
RETURN material, concept, user