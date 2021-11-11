MATCH (workspace:Workspace)<-[:USER_OWN]-(user:User{userId: $userId})
WHERE workspace.deltaGraphId CONTAINS replace($courseCode,' ' ,'_')
WITH DISTINCT workspace
MATCH (subject)<-[:WORK_ON]-(workspace)
WITH subject, workspace
MATCH (wh:GraphConcept)-[wr:DELTA_GRAPH_RELATIONSHIP{deltaGraphId: $deltaGraphId}]->(wt:GraphConcept)
WITH DISTINCT wr, DISTINCT wh, DISTINCT wt, workspace, DISTINCT subject
OPTIONAL MATCH (wh)-[sr:DELTA_GRAPH_RELATIONSHIP{deltaGraphId: subject.deltaGraphId}]->(wt)
WITH
    wr,
    CASE sr <> null
    THEN sr
    ELSE {value: null}
    END as sr
WHERE
    wr.value <> sr.value AND
    NOT (
        wr.value == false AND 
        sr.value == null
        )
MERGE (subject)<-[:FORK]-(branch:Branch:DeltaGraph)
SET branch.creationDate = datetime.transaction(),
    branch.deltaGraphId = split(subject.deltaGraphId,'.')[0] + '.' + id(branch),
    branch.tag = $tag
MERGE (wh)-[fr:DELTA_GRAPH_RELATIONSHIP{name: wr.name, deltaGraphId: branch.deltaGraphId}]-> (wt)
SET
    fr.creationDate = datetime.transaction(),
    fr.value = wr.value