MERGE (courseConcept:GraphConcept{name: $name})
MERGE (course:Course)-[:COURSE_DESCRIBE]->(courseConcept)
SET course.imageURL = $imageURL, course.courseName = $courseName, course.isInternal = true
MERGE (course)<-[:TRUNK_DESCRIBE]-(trunk:Trunk:DeltaGraph)
SET trunk.creationDate = datetime.transaction(),
    trunk.deltaGraphId = toString(id(course)) + '.' + id(trunk),
    trunk.tag = 'init'
WITH course
MATCH (instructor:User{userId: $userId})-[:PRIVILEGED_OF]->(:Permission{canJoinCourse: true})
MERGE (instructor)-[:USER_TEACH]->(course)