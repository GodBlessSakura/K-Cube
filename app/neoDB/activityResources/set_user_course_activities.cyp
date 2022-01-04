MATCH (user:User{userId: $userId}), (course:Course)-[:COURSE_DESCRIBE]->(courseConcept{name: $courseCode})
WHERE
    EXISTS((user)-[:PRIVILEGED_OF]->(:Permission{canWriteAllCourseMaterial: true})) or
    EXISTS((user)-[:USER_TEACH]->(course))
WITH DISTINCT user, course
MATCH (concept:GraphConcept{name: $name})
MERGE (concept)<-[:ACTIVITY_OF]-(activity:Activity{courseNodeId: id(course)})<-[:INSTRUCTOR_CREATE]-(user)
SET
    activity.desc = $desc
    activity.week = $week
RETURN activity