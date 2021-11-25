
MATCH (course)-[:COURSE_DESCRIBE]->(:GraphConcept{name: $courseCode})
WITH DISTINCT course
MATCH (course)<-[describe:BRANCH_DESCRIBE]-()<-[:USER_OWN]-(user:User)
RETURN user