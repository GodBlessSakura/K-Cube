MATCH (user:User{userId: $userId})-[:PRIVILEGED_OF]->(:Permission{canGiveFeedback: true})
WITH DISTINCT user
MATCH (feedback:Feedback)
WHERE id(feedback) = toInteger($id)
MERGE (user)-[reply:USER_REPLYING]->(feedback:Feedback)
SET
    reply.creationDate = datetime.transaction(),
    reply.text = $text
RETURN reply
