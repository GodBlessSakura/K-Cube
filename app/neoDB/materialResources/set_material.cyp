MATCH (:GraphConcept{name: $name})<-[:CONTENT_DESCRIBE]-(material:Material{courseCode: $courseCode})<-[:INSTRUCTOR_CREATE]-(:User{userId: $userId})
SET
    material.url = $url,
    material.desc = $desc
RETURN material, concept
