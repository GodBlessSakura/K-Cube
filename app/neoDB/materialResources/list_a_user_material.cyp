MATCH (concept:GraphConcept)<-[:CONTENT_DESCRIBE]-(material:Material{courseCode: $courseCode})<-[:INSTRUCTOR_CREATE]-(:User{userId: $userId})
RETURN material, concept