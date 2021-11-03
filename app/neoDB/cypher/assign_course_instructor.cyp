MATCH
    (instructor:User{userId: $userId})-[:PRIVILEGED_OF]->(:Permission{canBeAssignedCourse: true}),
    (course)-[:COURSE_DESCRIBE]->(:GraphConcept{name: $courseCode})
MERGE (instructor)-[:USER_TEACH]->(course)