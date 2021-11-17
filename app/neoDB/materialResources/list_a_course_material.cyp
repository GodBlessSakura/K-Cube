MATCH (concept:GraphConcept)<-[:CONTENT_DESCRIBE]-(material:Material{courseCode: $courseCode})<-[:INSTRUCTOR_CREATE]-(user:User)
RETURN material, concept, user