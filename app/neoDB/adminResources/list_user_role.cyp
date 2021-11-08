MATCH (user:User)-[:PRIVILEGED_OF]->(permission:Permission)
RETURN user, collect(permission.role) as roles