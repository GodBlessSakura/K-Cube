MERGE (courseConcept:GraphConcept{name: $name})
MERGE (course:Course)-[:COURSE_DESCRIBE]->(courseConcept)
SET course.imageURL = $imageURL, course.displayName = $displayName
RETURN course, courseConcept