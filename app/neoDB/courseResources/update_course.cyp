MATCH (courseConcept:GraphConcept{name: $courseCode})
SET courseConcept.name = $name
MATCH (course:Course)-[:COURSE_DESCRIBE]->(courseConcept)
SET course.imageURL = $imageURL, course.courseName = $courseName
MERGE (course)<-[:TRUNK_DESCRIBE]-(trunk:Trunk:DeltaGraph)