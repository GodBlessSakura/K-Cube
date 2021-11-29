MATCH (courseConcept:GraphConcept{name: $courseCode})
MATCH (course:Course)-[:COURSE_DESCRIBE]->(courseConcept)
SET courseConcept.name = $name
SET course.imageURL = $imageURL, course.courseName = $courseName