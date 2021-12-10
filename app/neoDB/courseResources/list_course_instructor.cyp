
MATCH (user:User)
WHERE EXISTS((user)-[:PRIVILEGED_OF]->(:Permission{canJoinCourse: true})) OR EXISTS((user)-[:USER_TEACH]->()-[:COURSE_DESCRIBE]->(:GraphConcept{name: $courseCode}))
RETURN user.userId as userId, EXISTS((user)-[:USER_TEACH]->()-[:COURSE_DESCRIBE]->(:GraphConcept{name: $courseCode})) as isAssigned