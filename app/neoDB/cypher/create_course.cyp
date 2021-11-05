MERGE (courseConcept:GraphConcept{name: $name})
MERGE (course:Course)-[:COURSE_DESCRIBE]->(courseConcept)
SET course.imageURL = $imageURL, course.displayName = $displayName
MERGE (course)<-[:TRUNK_DESCRIBE]-(trunk:Trunk:DeltaGraph)
SET trunk.creationDate = datetime.transaction(),
    trunk.deltaGraphId = replace($name,' ' ,'_') + '.' + id(trunk),
    trunk.cachedGraphId = replace($name,' ' ,'_') + '.' + id(trunk),
    trunk.tag = 'init'