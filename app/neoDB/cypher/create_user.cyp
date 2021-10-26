MATCH (permission:Permission{role: 'restricted'})
CREATE (permission)<-[permission_grant:PRIVILEGED_OF]-(user:User {userId: $userId, userName: $userName, email: $email})
-[password_set:AUTHENTICATED_BY]->(:Credential {saltedHash: $saltedHash})
SET
password_set.creationDate = timestamp(),
permission_grant.creationDate = timestamp()
RETURN user;