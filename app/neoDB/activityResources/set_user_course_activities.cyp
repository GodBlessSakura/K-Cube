MATCH (user:User{userId: $userId}), (course:Course)-[:COURSE_DESCRIBE]->(courseConcept{name: $courseCode})
WHERE
    EXISTS((user)-[:PRIVILEGED_OF]->(:Permission{canWriteAllCourseMaterial: true})) or
    EXISTS((user)-[:USER_TEACH]->(course))
WITH DISTINCT user, course
MATCH (concept:GraphConcept{name: $name})
MERGE (concept)<-[:ACTIVITY_OF]-(activity:Activity:GraphAttribute)<-[:INSTRUCTOR_CREATE]-(user)
MERGE (activity)-[:ATTRIBUTE_FROM]->(course)
SET
    activity.desc = $desc,
    activity.week = $week
RETURN activity