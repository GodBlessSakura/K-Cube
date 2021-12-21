MERGE (courseConcept:GraphConcept{name: $name})
WITH courseConcept
CALL{
    WITH courseConcept
    WITH courseConcept
    WHERE NOT EXISTS(()-[:COURSE_DESCRIBE]->(courseConcept))
    RETURN null
}
WITH DISTINCT courseConcept
MERGE (course:Course)-[:COURSE_DESCRIBE]->(courseConcept)
SET course.imageURL = $imageURL, course.courseName = $courseName, course.isInternal = true
MERGE (course)<-[:TRUNK_DESCRIBE]-(trunk:Trunk:DeltaGraph)
SET trunk.creationDate = datetime.transaction(),
    trunk.deltaGraphId = toString(id(course)) + '.' + id(trunk),
    trunk.tag = 'init'
WITH course
MATCH (instructor:User{userId: $userId})-[:PRIVILEGED_OF]->(:Permission{canJoinCourse: true})
MERGE (instructor)-[:USER_TEACH]->(course)
RETURN course