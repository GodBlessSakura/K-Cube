MATCH (course:Course)-[:COURSE_DESCRIBE]->(courseConcept{name: $courseCode}),(concept:GraphConcept{name: $name})
WITH course, concept
    MERGE (newConcept:GraphConcept{name: $newName})
    MERGE (concept)-[:DELTA_GRAPH_DISAMBIGUATION{
        creationDate: datetime.transaction(), userId: $userId, courseCode:$courseCode
    }]->(newConcept)
WITH course, concept, newConcept
CALL{
    WITH course, concept, newConcept
    MATCH (concept)-[r:DELTA_GRAPH_RELATIONSHIP]->(theOther:GraphConcept)
    WHERE split(r.deltaGraphId,'.')[0] = toString(id(course))
    MERGE (newConcept)-[newR:DELTA_GRAPH_RELATIONSHIP{
        name: r.name, deltaGraphId: r.deltaGraphId, creationDate:  r.creationDate, value: r.value
        }]->(theOther)
    DELETE r
    RETURN null
UNION
    WITH course, concept, newConcept
    MATCH (concept)<-[r:DELTA_GRAPH_RELATIONSHIP]-(theOther:GraphConcept)
    WHERE split(r.deltaGraphId,'.')[0] = toString(id(course))
    MERGE (newConcept)<-[newR:DELTA_GRAPH_RELATIONSHIP{
        name: r.name, deltaGraphId: r.deltaGraphId, creationDate:  r.creationDate, value: r.value
        }]-(theOther)
    DELETE r
    RETURN null
UNION
    WITH concept, newConcept, course
    MATCH (concept)<-[rs:ACTIVITY_OF]-(attr:Activity)-[:ATTRIBUTE_FROM]->(course)
    WITH newConcept, collect(rs) as rs, attr
    FOREACH (r in rs |
        MERGE (newConcept)<-[:ACTIVITY_OF]-(attr)
        DELETE r
    )
    RETURN null
UNION
    WITH concept, newConcept, course
    MATCH (concept)<-[rs:CONTENT_DESCRIBE]-(attr:Material)-[:ATTRIBUTE_FROM]->(course)
    WITH newConcept, collect(rs) as rs, attr
    FOREACH (r in rs |
        MERGE (newConcept)<-[:CONTENT_DESCRIBE]-(attr)
        DELETE r
    )
    RETURN null
}
RETURN newConcept as concept