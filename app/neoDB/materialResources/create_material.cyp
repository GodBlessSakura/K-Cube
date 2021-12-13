MATCH (user:User{userId: $userId}), (course:GraphConcept{name: $courseCode})
WHERE
    EXISTS((user)-[:PRIVILEGED_OF]->(:Permission{canWriteAllCourseMaterial: true})) or
    EXISTS((course)<-[:USER_TEACH]-(user)-[:PRIVILEGED_OF]->(:Permission{canWriteTeachingCourseMaterial: true}))
WITH DISTINCT user, course
MATCH (concept:GraphConcept{name: $name})
MERGE (concept)<-[:CONTENT_DESCRIBE]-(material:Material{courseCode: course.name})<-[:INSTRUCTOR_CREATE]-(user)
SET
    material.url = $url,
    material.desc = $desc
RETURN material, concept
