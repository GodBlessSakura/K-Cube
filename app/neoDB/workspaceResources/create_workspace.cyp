MATCH (parent{deltaGraphId: $deltaGraphId}),(owner:User{userId: $userId})
CREATE (parent)<-[:WORK_ON]-(workspace:Workspace)<-[:USER_OWN]-(owner)
SET
    workspace.creationDate = datetime.transaction(),
    workspace.deltaGraphId = split(parent.deltaGraphId,'.')[0] + '.' + id(workspace),
    workspace.tag = $tag
RETURN workspace.deltaGraphId as deltaGraphId;