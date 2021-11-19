MATCH (branch:Branch{deltaGraphId: $deltaGraphId})<-[:USER_OWN]-(user:User{userId: $userId})
SET branch.visibility = 
    CASE branch.visibility < toInteger($visibility)
        WHEN true THEN toInteger($visibility)
        ELSE branch.visibility
    END
WITH DISTINCT branch
MATCH p = (ancestor)<-[:PATCH*]-(branch)
WITH collect(ancestor) + [branch] AS list, branch
CALL{
    WITH list
    UNWIND list as graph
    RETURN max(graph.visibility) as visibility
}
UNWIND list as graph
SET graph.visibility = visibility
RETURN branch