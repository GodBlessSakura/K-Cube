CREATE CONSTRAINT user_uid_constraint IF NOT EXISTS ON (n:User) ASSERT n.userId IS UNIQUE;
CREATE CONSTRAINT user_email_constraint IF NOT EXISTS ON (n:User) ASSERT n.email IS UNIQUE;
CREATE CONSTRAINT permission_uid_constraint IF NOT EXISTS ON (n:Permission) ASSERT n.role IS UNIQUE;
CREATE CONSTRAINT draft_uid_constraint IF NOT EXISTS ON (n:Draft) ASSERT n.draftId IS UNIQUE;
CREATE CONSTRAINT course_uid_constraint IF NOT EXISTS ON (n:Course) ASSERT n.displayName IS UNIQUE;
CREATE CONSTRAINT GraphConcept_uid_constraint IF NOT EXISTS ON (n:GraphConcept) ASSERT n.name IS UNIQUE;
CREATE CONSTRAINT GraphRelationship_uid_constraint IF NOT EXISTS ON (n:GraphRelationship) ASSERT n.name IS UNIQUE;
CREATE CONSTRAINT job_uid_constraint IF NOT EXISTS ON (n:Job) ASSERT n.jobId IS UNIQUE;
CREATE CONSTRAINT student_uid_constraint IF NOT EXISTS ON (n:Student) ASSERT n.studentId IS UNIQUE;

//create permission and user
MERGE (:Permission {
    role: "admin",
    canCreateGraphConcept: true,
    canCreateCourse: true,
    canCreateJob: true,
    canCreateDraft: true,
    canProposeRelationship: true,
    canApproveRelationship: true,
    canOperateDraftForOthers: true,
    canUploadPhoto: true,
    canOwnDraft: true
});
MERGE (:Permission {
    role: "teacher",
    canCreateGraphConcept: true,
    canCreateCourse: false,
    canCreateJob: false,
    canCreateDraft: true,
    canProposeRelationship: true,
    canApproveRelationship: false,
    canOperateDraftForOthers: false,
    canUploadPhoto: false,
    canOwnDraft: true
})
MERGE (:Permission {
    role: "restricted",
    canCreateGraphConcept: false,
    canCreateCourse: false,
    canCreateJob: false,
    canCreateDraft: false,
    canProposeRelationship: false,
    canApproveRelationship: false,
    canOperateDraftForOthers: false,
    canUploadPhoto: false,
    canOwnDraft: false
});


:param userId => "bob2021";
:param userName => "bob.J";
:param email => "bob@polyu.fake.hk";
:param saltedHash => "1234";
MATCH (permission:Permission{role: "restricted"})
CREATE (permission)<-[permission_grant:PRIVILEGED_OF]-(user:User {userId: $userId, userName: $userName, email: $email})-[password_set:AUTHENTICATED_BY]->(:Credential {saltedHash: $saltedHash})
SET 
    password_set.creationDate = timestamp(),
    permission_grant.creationDate = timestamp()
RETURN user;

//give user a role
MATCH
    (permission:Permission{role: $role}),
    (user:User{userId: $userId})
MERGE (permission)<-[permission_grant:PRIVILEGED_OF]-(user)
ON CREATE 
    SET 
        permission_grant.creationDate = timestamp()
RETURN user, permission_grant, permission;

//create course
:param userId => "jerry2021";
:param course_name => "Introduction of computer science";
:param imageURL => '../static/image.jpg';
:param course_code => "COMP0001";
MATCH (:User{userId: $userId})-[:PRIVILEGED_OF]->(:Permission{canCreateCourse:true, canCreateGraphConcept:true})
MERGE (courseConcept:GraphConcept{name: $course_code})
MERGE (course:Course{displayName: $course_name, imageURL: $imageURL})-[:COURSE_DESCRIBE]->(courseConcept)


//create GraphConcepts
:param userId => "alice1234";
MATCH (:User{userId:$userId})-[:PRIVILEGED_OF]->(:Permission{canCreateGraphConcept:true})
MERGE (:GraphConcept{name: "COMP0001"})
MERGE (:GraphConcept{name: "data structure"})
MERGE (:GraphConcept{name: "tree algorithm"});

//create admin defind graph relationships
:param userId => 'jerry2021';
:param r_name => 'related';
MATCH (approver:User{userId: $userId})-[:PRIVILEGED_OF]->(:Permission {canProposeRelationship: true, canApproveRelationship: true})
MERGE (r:GraphRelationship{name: $r_name})
MERGE (r)<-[:USER_APPROVE]-(approver);

//create user defined graph relationships
:param userId => 'alice1234';
:param r_name => 'further reading';
MATCH (proposer:User{userId: $userId})-[:PRIVILEGED_OF]->(:Permission {canProposeRelationship: true})
MERGE (r:GraphRelationship{name:  $r_name})
MERGE (r)<-[:USER_PROPOSE]-(proposer);

//approve a proposed graph relationships
:param userId => 'jerry2021';
:param r_name => 'further reading';
MATCH (approver:User{userId: $userId})-[:PRIVILEGED_OF]->(:Permission {canApproveRelationship: true})
MATCH (r:GraphRelationship{name: $r_name})
MERGE (r)<-[:USER_APPROVE]-(approver);

//create draft
:param draftName => "draft 123";
:param userId => 'alice';
:param courseCode => "COMP0001";
MATCH
    (owner:User{userId: $userId})-[:PRIVILEGED_OF]-(:Permission{canCreateDraft: true, canOwnDraft: true}),
    (course:Course)-[:COURSE_DESCRIBE]->(:GraphConcept{name: $courseCode})
MERGE (owner)-[:USER_OWN]->(draft:Draft)-[:DRAFT_DESCRIBE]->(course)-[:COURSE_DESCRIBE]->(courseConcept)
ON CREATE
    set 
        draft.draftId = owner.userId + "." + replace($courseConcept.name," ", "_") + "." + replace($draftName," ", "_"),
        draft.name = $draftName,
        draft.creationDate = timestamp(),
        draft.lastModified = timestamp(),
        draft.status = "unpublished"
RETURN draft;

//create draft for others
:param draftName => "draft 123";
:param operatorId => 'jerry2021';
:param ownerId -> 'alice1234';
:param courseCode => "COMP0001";
MATCH
    (:User{userId: $operatorId})-[:PRIVILEGED_OF]-(:Permission{canCreateDraft: true, canOperateDraftForOthers: true}),
    (owner:User{userId: $ownerId})-[:PRIVILEGED_OF]-(:Permission{canOwnDraft: true}),
    (:Course)<-[:COURSE_DESCRIBE]->(:GraphConcept{name: courseCode})
MERGE (owner)-[:USER_OWN]->(draft:Draft)-[:DRAFT_DESCRIBE]->(course)
ON CREATE
    set 
        draft.draftId = owner.userId + "." + replace($draftName," ", "_"),
        draft.draftName = $draftName,
        draft.creationDate = timestamp(),
        draft.lastModified = timestamp(),
        draft.status = "unpublished"
RETURN draft;

//create triples for draft that may create node
:param draftId => "alice1234.draft_123";
:param userId => 'alice1234';
:param h_name => 'COMP0001';
:param r_name => 'related';
:param t_name => 'data type'
MATCH
    (draft:Draft{draftId: $draftId})<-[:USER_OWN]-(:User{userId: $userId})-[:PRIVILEGED_OF]->(:Permission{canOwnDraft: true, canCreateGraphConcept: true}),
    (approved_graph_relationship:GraphRelationship{name: $r_name})<-[:USER_APPROVE]-(:User)-[:PRIVILEGED_OF]->(:Permission{canApproveRelationship: true})
MERGE (h:GraphConcept{name: $h_name})
MERGE (t:GraphConcept{name: $t_name})
MERGE (h) -[r:GRAPH_RELATIONSHIP{name: approved_graph_relationship.name}]-> (t)
SET
    draft.lastModified = timestamp(),
    r.creationDate = timestamp(),
    r.draftId = draft.draftId
RETURN draft;

//create triples for others; draft that may create node
:param draftId => "alice1234.draft_123";
:param operatorId => 'jerry2021';
:param ownerId -> 'alice1234';
:param h_name => 'COMP0001';
:param r_name => 'related';
:param t_name => 'data type'
MATCH
    (draft:Draft{draftId: $draftId})<-[:USER_OWN]-(:User{userId: $ownerId})-[:PRIVILEGED_OF]->(:Permission{canOwnDraft: true}),
    (:User{userId: $operatorId})-[:PRIVILEGED_OF]->(:Permission{canCreateGraphConcept: true, canCreateDraftForOthers: true}),
    (approved_graph_relationship:GraphRelationship{name: $r_name})<-[:USER_APPROVE]-(:User)-[:PRIVILEGED_OF]->(:Permission{canApproveRelationship: true})
MERGE (h:GraphConcept{name: $h_name})
MERGE (t:GraphConcept{name: $t_name})
MERGE (h) -[r:GRAPH_RELATIONSHIP{name: approved_graph_relationship.name, r.draftId = draft.draftId}]-> (t)
ON CREATE
    SET
        draft.lastModified = timestamp(),
        r.creationDate = timestamp(),
RETURN draft;


//public graph
:param want_status => "published";
MATCH (selected_draft:Draft{status: $want_status})
WITH selected_draft.draftId as published_id
CALL {
    WITH published_id
    MATCH (h:GraphConcept)-[r:GRAPH_RELATIONSHIP{draftId: published_id}]->(t:GraphConcept)
    RETURN h.name, r.name, t.name , count(*) AS vote
}
RETURN *;

//publish a draft
:param userId => 'alice1234'
:param draftId => "alice1234.draft 123"
MATCH
    (draft:Draft{draftId: $draftId})<-[:USER_OWN]-(:User{userId: $userId})
SET draft.status = "published"
RETURN draft;