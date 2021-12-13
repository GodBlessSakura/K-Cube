MATCH (courseConcept:GraphConcept{name: $courseCode})
MATCH (course:Course)-[:COURSE_DESCRIBE]->(courseConcept)
OPTIONAL MATCH (material:Material{courseCode: $courseCode})
SET material.courseCode = $name
SET courseConcept.name = $name
SET course.imageURL = $imageURL, course.courseName = $courseName
