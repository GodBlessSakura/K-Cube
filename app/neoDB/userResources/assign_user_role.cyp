MATCH
(permission:Permission{role: $role}),
(user:User{userId: $userId, verified: true})
MERGE (permission)<-[permission_grant:PRIVILEGED_OF]-(user)
ON CREATE
SET
permission_grant.creationDate = datetime.transaction(),
permission_grant.message = $message
RETURN user, permission_grant, permission;