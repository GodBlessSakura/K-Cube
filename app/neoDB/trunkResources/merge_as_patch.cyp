MATCH (user:User{userId: $userId})-[:PRIVILEGED_OF]->(:Permission{canWriteTrunk: true})
WITH DISTINCT user
MATCH (overwritee:Trunk{deltaGraphId: $overwriteeId})
WHERE NOT EXISTS((overwritee)<-[:PATCH]-())
WITH DISTINCT user, overwritee
MATCH (overwriter:Branch{deltaGraphId: $overwriterId}), (course:Course)
WHERE toString(id(course)) = split($overwriterId,'.')[0]
WITH 
    overwriter,
    user,
    overwritee,
    EXISTS((user)-[:PRIVILEGED_OF]->(:Permission{role:'DLTC'})) as isDLTC,
    EXISTS((user)-[:PRIVILEGED_OF]->(:Permission{role:'instructor'})) as isInstructor,
    EXISTS((user)-[:USER_TEACH]->(course)) as isAssigned
WHERE        
    (overwriter.visibility = 4) OR
    (overwriter.visibility = 3 AND (isDLTC OR isInstructor)) OR
    (overwriter.visibility = 2 AND isInstructor) OR
    (overwriter.visibility = 1 AND isAssigned) OR
    EXISTS((overwriter)<-[:USER_OWN]-(user))
WITH user, overwriter, overwritee
CREATE
    (overwritee)<-[:PATCH]-(trunk:Trunk:DeltaGraph),
    (trunk)-[:TRUNK_PULL]->(overwriter)
SET 
    trunk.deltaGraphId = split(overwritee.deltaGraphId,'.')[0]  + '.' + id(trunk),
    trunk.tag = $tag
WITH overwritee, trunk
MATCH (wh:GraphConcept)-[wr:DELTA_GRAPH_RELATIONSHIP{deltaGraphId: $overwriterId}]->(wt:GraphConcept)
WITH wr, wh, wt, trunk, overwritee
CALL{
    WITH wr, wh, wt, trunk, overwritee
    OPTIONAL MATCH (wh)-[sr:DELTA_GRAPH_RELATIONSHIP{deltaGraphId: overwritee.deltaGraphId}]->(wt)
    WITH
        wr, wh, wt, trunk, overwritee,
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
    MERGE (wh)-[fr:DELTA_GRAPH_RELATIONSHIP{name: wr.name, deltaGraphId: trunk.deltaGraphId}]-> (wt)
    SET
        fr.creationDate = datetime.transaction(),
        fr.value = wr.value
    RETURN null
UNION
    WITH trunk, overwritee
    MATCH (sh:GraphConcept)-[sr:DELTA_GRAPH_RELATIONSHIP{deltaGraphId: overwritee.deltaGraphId}]->(st:GraphConcept)
    MERGE (sh) -[fr:DELTA_GRAPH_RELATIONSHIP{name: sr.name, deltaGraphId: trunk.deltaGraphId}]-> (st)
    ON CREATE SET
        fr.creationDate = datetime.transaction(),
        fr.value = sr.value
    RETURN null
}
RETURN DISTINCT trunk