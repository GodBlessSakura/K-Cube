MATCH (draft:Draft{draftId: $draftId})<-[:USER_OWN]-(owner:User{userId: $userId})-[:PRIVILEGED_OF]-(:Permission{canCreateDraft: true, canOwnDraft: true})
WITH DISTINCT draft
SET draft.status = $status
RETURN draft.status;