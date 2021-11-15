MATCH (user)-[:USER_OWN]->(overwritee{deltaGraphId: $overwriteeId})
WITH DISTINCT overwritee, user
CALL{
    WITH user
    MATCH (overwriter:Branch{deltaGraphId: $overwriterId})
    WITH 
        overwriter,
        user,
        EXISTS((user)-[:PRIVILEGED_OF]->(:Permission{role:'DLTC'})) as isDLTC,
        EXISTS((user)-[:PRIVILEGED_OF]->(:Permission{role:'instructor'})) as isInstructor,
        EXISTS((user)-[:USER_TEACH]->()-[:COURSE_DESCRIBE]->(:GraphConcept{name: split(overwriter.deltaGraphId,'.')[0]})) as isAssigned
    WHERE        
        (overwriter.visibility = 'public') OR
        (overwriter.visibility = 'colleague' AND (isDLTC OR isInstructor)) OR
        (overwriter.visibility = 'instructor' AND isInstructor) OR
        (overwriter.visibility = 'collaborator' AND isAssigned) OR
        EXISTS((overwriter)<-[:USER_OWN]-(user))
    RETURN overwriter
UNION
    MATCH (overwriter:Trunk{deltaGraphId: $overwriterId})
    RETURN overwriter
}
WITH overwriter, overwritee, user
CREATE
    (overwritee)<-[:PATCH]-(branch:Branch:DeltaGraph)<-[:USER_OWN]-(user),
    (branch)-[:BRANCH_PULL]->(overwriter)
SET 
    branch.visibility = 
        CASE overwritee.visibility
            WHEN null
            THEN 'private'
            ELSE overwritee.visibility
            END,
    branch.creationDate = datetime.transaction(),
    branch.deltaGraphId = split(overwritee.deltaGraphId,'.')[0] + '.' + id(branch),
    branch.tag = $tag
WITH overwritee, branch
MATCH (wh:GraphConcept)-[wr:DELTA_GRAPH_RELATIONSHIP{deltaGraphId: $overwriterId}]->(wt:GraphConcept)
WITH wr, wh, wt, branch, overwritee
CALL{
    WITH wr, wh, wt, branch, overwritee
    OPTIONAL MATCH (wh)-[sr:DELTA_GRAPH_RELATIONSHIP{deltaGraphId: overwritee.deltaGraphId}]->(wt)
    WITH
        wr, wh, wt, branch, overwritee,
        CASE sr
            WHEN null
            THEN {value: 'null'}
            ELSE sr
            END as sr
    WHERE
        wr.value <> sr.value AND
        NOT (
            wr.value = false AND 
            sr.value = 'null'
            )
    MERGE (wh)-[fr:DELTA_GRAPH_RELATIONSHIP{name: wr.name, deltaGraphId: branch.deltaGraphId}]-> (wt)
    SET
        fr.creationDate = datetime.transaction(),
        fr.value = wr.value
    RETURN null
UNION
    WITH branch, overwritee
    MATCH (sh:GraphConcept)-[sr:DELTA_GRAPH_RELATIONSHIP{deltaGraphId: overwritee.deltaGraphId}]->(st:GraphConcept)
    MERGE (sh) -[fr:DELTA_GRAPH_RELATIONSHIP{name: sr.name, deltaGraphId: branch.deltaGraphId}]-> (st)
    ON CREATE SET
        fr.creationDate = datetime.transaction(),
        fr.value = sr.value
    RETURN null
}
RETURN DISTINCT branch