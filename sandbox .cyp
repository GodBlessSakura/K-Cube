CREATE CONSTRAINT user_uid_constraint IF NOT EXISTS ON (n:User) ASSERT n.userId IS UNIQUE;
CREATE CONSTRAINT permission_uid_constraint IF NOT EXISTS ON (n:Permission) ASSERT n.role IS UNIQUE;
CREATE CONSTRAINT draft_uid_constraint IF NOT EXISTS ON (n:Draft) ASSERT n.draftId IS UNIQUE;
CREATE CONSTRAINT concept_uid_constraint IF NOT EXISTS ON (n:Concept) ASSERT n.name IS UNIQUE;
CREATE CONSTRAINT proposed_graph_relationship_name_uid_constraint IF NOT EXISTS ON (n:ProposedGraphRelationshipName) ASSERT n.name IS UNIQUE;
CREATE CONSTRAINT job_uid_constraint IF NOT EXISTS ON (n:Job) ASSERT n.jobId IS UNIQUE;
CREATE CONSTRAINT student_uid_constraint IF NOT EXISTS ON (n:Student) ASSERT n.studentId IS UNIQUE;

//create permission and user
CREATE (:Permission {
    role: "admin",
    canCreateConcept: true,
    canCreateCourse: true,
    canCreateJob: true,
    canCreateDraft: true,
    canProposeRelationship: true,
    canApproveProposal: true,
    canCreateDraftForOthers: true
}),(:Permission {
    role: "teacher",
    canCreateConcept: true,
    canCreateCourse: false,
    canCreateJob: false,
    canCreateDraft: true,
    canProposeRelationship: true,
    canApproveProposal: false,
    canCreateDraftForOthers: false
}),(:Permission {
    role: "student",
    canCreateConcept: false,
    canCreateCourse: false,
    canCreateJob: false,
    canCreateDraft: false,
    canProposeRelationship: false,
    canApproveProposal: false,
    canCreateDraftForOthers: false
});


MATCH (permission:Permission{role: "admin"})
MERGE (permission)<-[permission_grant:WEB_HAS_PERMISSION]-(user:User {userId: "jerry2021", userName:"jerry.C", email:"jerry@polyu.fake.hk"})
-[password_set:WEB_IS_AUTHENTICATED_BY]->(:Credential {saltedHash: "1234"})
ON CREATE 
    SET 
        password_set.creationDate = timestamp(),
        permission_grant.creationDate = timestamp()
RETURN user;

MATCH (permission:Permission{role: "teacher"})
MERGE (permission)<-[permission_grant:WEB_HAS_PERMISSION]-(user:User {userId: "alice1234", userName:"alice.J", email:"alice@polyu.fake.hk"})
-[password_set:WEB_IS_AUTHENTICATED_BY]->(:Credential {saltedHash: "1234"})
ON CREATE 
    SET 
        password_set.creationDate = timestamp(),
        permission_grant.creationDate = timestamp()
RETURN user;

MATCH (permission:Permission{role: "student"})
MERGE (permission)<-[permission_grant:WEB_HAS_PERMISSION]-(user:User {userId: "bob2021", userName:"bob.J", email:"bob@polyu.fake.hk"})
-[password_set:WEB_IS_AUTHENTICATED_BY]->(:Credential {saltedHash: "1234"})
ON CREATE 
    SET 
        password_set.creationDate = timestamp(),
        permission_grant.creationDate = timestamp()
RETURN user;

//create course
:param userId => "jerry2021";
:param course_name => "Introduction of computer science"
:param course_code => "COMP0001"
MATCH (:User{userId:"jerry2021"})-[:WEB_HAS_PERMISSION]->(:Permission{canCreateCourse:true,canCreateConcept:true})
MERGE (course_concept:Concept{name: $course_code})
MERGE (course:Course{displayName: $course_name})<-[:WEB_DESCRIBE_COURSE]-(course_concept);

//create concepts
:param userId => "alice1234";
MATCH (:User{userId:$userId})-[:WEB_HAS_PERMISSION]->(:Permission{canCreateConcept:true})
MERGE (:Concept{name: "COMP0001"})
MERGE (:Concept{name: "data structure"})
MERGE(:Concept{name: "tree algorithm"});

//create admin defind graph relationships
:param userId => 'jerry2021';
:param r_name => 'related';
MATCH (approver:User{userId: $userId})-[:WEB_HAS_PERMISSION]->(:Permission {canApproveProposal: true})
MERGE (r:ProposedGraphRelationshipName{name: $r_name})
MERGE (r)<-[:WEB_APPROVE]-(approver);

//create user defined graph relationships
:param userId => 'alice1234';
:param r_name => 'further reading';
MATCH (proposer:User{userId: $userId})-[:WEB_HAS_PERMISSION]->(:Permission {canProposeRelationship: true})
MERGE (r:ProposedGraphRelationshipName{name:  $r_name})
MERGE (r)<-[:WEB_PROPOSE]-(proposer);

//approve an user defined graph relationships
:param userId => 'jerry2021';
:param r_name => 'further reading';
MATCH (approver:User{userId: $userId})-[:WEB_HAS_PERMISSION]->(:Permission {canApproveProposal: true})
MERGE (r:ProposedGraphRelationshipName{name: $r_name})
MERGE (r)<-[:WEB_APPROVE]-(approver);

//create draft
:param draftName => "draft 123";
:param userId => 'alice1234';
:param courseCode => "COMP0001"
MATCH
    (user:User{userId: $userId})-[:WEB_HAS_PERMISSION]-(:Permission{canCreateDraft: true}),
    (course:Course)<-[:WEB_DESCRIBE_COURSE]-(:Concept{name: courseCode})
MERGE (user)-[:WEB_OWN]->(draft:Draft)-[:WEB_DESCRIBE_COURSE]->(course)
ON CREATE
    set 
        draft.draftId = user.userId + "." + $draftName,
        draft.name = $draftName,
        draft.creationDate = timestamp(),
        draft.lastModified = timestamp(),
        draft.published = false
RETURN draft;

//create triples for draft that may create node
:param draftId => "alice1234.draft 123";
:param userId => 'alice1234';
:param h_name => 'COMP0001';
:param r_name => 'related';
:param t_name => 'data type'
MATCH
    (draft:Draft{draftId: $draftId})<-[:WEB_OWN]-(:User{userId: $userId})-[:WEB_HAS_PERMISSION]->(:Permission{canCreateConcept: true}),
    (approved_r:ProposedGraphRelationshipName{name: $r_name})<-[:WEB_APPROVE]-(:User)-[:WEB_HAS_PERMISSION]->(:Permission{canApproveProposal: true})
MERGE (h:Concept{name: $h_name})
MERGE (t:Concept{name: $t_name})
MERGE (h) -[r:GRAPH_RELATIONSHIP{name: approved_r.name}]-> (t)
SET
    draft.lastModified = timestamp(),
    r.creationDate = timestamp(),
    r.draftId = draft.draftId
RETURN draft;

//create triples for draft that only use existing node
:param draftId => "alice1234.draft 123";
:param userId => 'alice1234';
:param h_name => 'COMP0001';
:param r_name => 'related';
:param t_name => 'data structure'
MATCH
    (draft:Draft{draftId: $draftId})<-[:WEB_OWN]-(:User{userId: $userId}),
    (approved_r:ProposedGraphRelationshipName{name: $r_name})<-[:WEB_APPROVE]-
    (:User)-[:WEB_HAS_PERMISSION]->(:Permission {canApproveProposal: true}),
    (h:Concept{name: $h_name}), (t:Concept{name: $t_name})
MERGE (h) -[r:GRAPH_RELATIONSHIP{name: approved_r.name}]-> (t) 
SET
    draft.lastModified = timestamp(),
    r.creationDate = timestamp(),
    r.draftId = draft.draftId
RETURN draft;

//create triples for draft that only use existing node !!! violate
:param draftId => "alice1234.draft 123";
:param userId => 'alice1234';
:param h_name => 'COMP0001';
:param r_name => 'related';
:param t_name => 'rocket science'
MATCH
    (draft:Draft{draftId: $draftId})<-[:WEB_OWN]-(:User{userId: $userId}),
    (approved_r:ProposedGraphRelationshipName{name: $r_name})<-[:WEB_APPROVE]-
    (:User)-[:WEB_HAS_PERMISSION]->(:Permission {canApproveProposal: true}),
    (h:Concept{name: $h_name}), (t:Concept{name: $t_name})
MERGE (h) -[r:GRAPH_RELATIONSHIP{name: approved_r.name}]-> (t) 
SET
    draft.lastModified = timestamp(),
    r.creationDate = timestamp(),
    r.draftId = draft.draftId
RETURN draft;

//public graph
:param want_published => true;
MATCH (published_draft:Draft{published: $want_published})
WITH published_draft.draftId as published_id
CALL {
    WITH published_id
    MATCH (h:Concept)-[r:GRAPH_RELATIONSHIP{draftId: published_id}]->(t:Concept)
    RETURN h , r, t , count(r.name) AS count
}
RETURN *;

//publish a draft
:param userId => 'alice1234'
MATCH
    (draft:Draft{draftId: "alice1234.draft 123"})<-[:WEB_OWN]-(:User{userId: $userId})
SET draft.published = true
RETURN draft;
