MATCH (user:User {userId: $userId})
SET
user.verified = CASE user.email = $email
    WHEN true THEN CASE EXISTS(user.verified)
        WHEN true THEN user.verified
        ELSE false
        END 
    ELSE false
    END,
user.userName = $userName,
user.email = $email
RETURN user;