MATCH (user:User{userId: $userId})-[:PRIVILEGED_OF]->(:Permission{canOwnDraft: true, canCreateGraphConcept: true})
WITH DISTINCT user
MATCH (draft:Draft{draftId: $draftId})<-[:USER_OWN]-(user)
WITH DISTINCT draft
MATCH (approved_graph_relationship:GraphRelationship{name: $r_name})<-[:USER_APPROVE]-(:User)-[:PRIVILEGED_OF]->(:Permission{canApproveRelationship: true})
WITH DISTINCT approved_graph_relationship, draft
MERGE (h:GraphConcept{name: $h_name})
MERGE (t:GraphConcept{name: $t_name})
MERGE (h) -[r:GRAPH_RELATIONSHIP{name: approved_graph_relationship.name, draftId: draft.draftId}]-> (t)
SET draft.lastModified = timestamp(),
r.creationDate = timestamp()
RETURN h.name, r.name, t.name;