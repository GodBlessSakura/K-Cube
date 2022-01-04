MATCH (course:Course)-[:COURSE_DESCRIBE]->(courseConcept{name: $courseCode})
MATCH (concept:GraphConcept)<-[:ACTIVITY_OF]-(activity:Activity{courseNodeId: id(course)})<-[:INSTRUCTOR_CREATE]-(user:User)
WHERE  EXISTS((user)-[:USER_TEACH]->()-[:COURSE_DESCRIBE]->(:GraphConcept{name: $courseCode}))
RETURN activity, concept, user