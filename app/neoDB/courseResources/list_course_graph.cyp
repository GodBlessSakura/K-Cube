
MATCH (course)-[:COURSE_DESCRIBE]->(:GraphConcept{name: $courseCode})
WITH DISTINCT course
MATCH (course)<-[:REPO_DESCRIBE]-(repo:Repository)<-[:USER_OWN]-(user:User)
WHERE EXISTS((user)-[:USER_TEACH]->(course))
RETURN user