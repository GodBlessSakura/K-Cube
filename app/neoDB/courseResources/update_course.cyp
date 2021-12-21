MATCH (courseConcept:GraphConcept{name: $courseCode})
WHERE NOT EXISTS(()-[:COURSE_DESCRIBE]->(courseConcept))
WITH DISTINCT courseConcept
MATCH (course:Course)-[:COURSE_DESCRIBE]->(courseConcept)
SET courseConcept.name = $name
SET course.imageURL = $imageURL, course.courseName = $courseName
RETURN course
