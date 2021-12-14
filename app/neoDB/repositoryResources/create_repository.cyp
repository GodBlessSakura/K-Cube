MATCH (user:User{userId: $userId})
WITH user
CALL{
    WITH user
    MATCH (graph:Branch{deltaGraphId: $deltaGraphId}), (course:Course)
    WHERE toString(id(course)) = split($deltaGraphId,'.')[0]
    WITH 
        graph,
        user,
        EXISTS((user)-[:PRIVILEGED_OF]->(:Permission{role:'DLTC'})) as isDLTC,
        EXISTS((user)-[:PRIVILEGED_OF]->(:Permission{role:'instructor'})) as isInstructor,
        EXISTS((user)-[:USER_TEACH]->(course)) as isTeaching,
        EXISTS((graph)<-[:USER_OWN]-(user)) as isOwner
    WHERE        
        (graph.visibility = 4) OR
        (graph.visibility = 3 AND (isDLTC OR isInstructor)) OR
        (graph.visibility = 2 AND isInstructor) OR
        (graph.visibility = 1 AND isTeaching) OR
        isOwner
    RETURN graph, isOwner
UNION
    MATCH (graph:Trunk{deltaGraphId: $deltaGraphId})
    RETURN graph, false as isOwner
}
CREATE
    (repo:Repository{tag: $tag}),
    (graph)<-[:FORK]-(branch:Branch:DeltaGraph)<-[:USER_OWN]-(user),
    (repo)<-[:USER_OWN]-(user),
    (repo)<-[:BRANCH_DESCRIBE]-(branch),
    (repo)<-[:BRANCH_CURSOR]-(branch)
SET 
    branch.visibility = 0,
    branch.creationDate = datetime.transaction(),
    branch.deltaGraphId = split(graph.deltaGraphId,'.')[0] + '.' + id(branch),
    repo.deltaGraphId = split(graph.deltaGraphId,'.')[0] + '.' + id(repo),
    branch.tag = $tag
WITH branch, graph
MATCH (sh:GraphConcept)-[sr:DELTA_GRAPH_RELATIONSHIP{deltaGraphId: graph.deltaGraphId}]->(st:GraphConcept)
MERGE (sh) -[fr:DELTA_GRAPH_RELATIONSHIP{name: sr.name, deltaGraphId: branch.deltaGraphId}]-> (st)
ON CREATE SET
    fr.creationDate = datetime.transaction(),
    fr.value = sr.value
RETURN branch