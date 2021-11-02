CREATE CONSTRAINT user_uid_constraint IF NOT EXISTS ON (n:User) ASSERT n.userId IS UNIQUE;
CREATE CONSTRAINT user_email_constraint IF NOT EXISTS ON (n:User) ASSERT n.email IS UNIQUE;
CREATE CONSTRAINT permission_uid_constraint IF NOT EXISTS ON (n:Permission) ASSERT n.role IS UNIQUE;
CREATE CONSTRAINT deltaGraph_uid_constraint IF NOT EXISTS ON (n:DeltaGraph) ASSERT n.deltaGraphId IS UNIQUE;
CREATE CONSTRAINT course_uid_constraint IF NOT EXISTS ON (n:Course) ASSERT n.displayName IS UNIQUE;
CREATE CONSTRAINT GraphConcept_uid_constraint IF NOT EXISTS ON (n:GraphConcept) ASSERT n.name IS UNIQUE;
CREATE CONSTRAINT GraphRelationship_uid_constraint IF NOT EXISTS ON (n:GraphRelationship) ASSERT n.name IS UNIQUE;
CREATE CONSTRAINT job_uid_constraint IF NOT EXISTS ON (n:Job) ASSERT n.jobId IS UNIQUE;
CREATE CONSTRAINT student_uid_constraint IF NOT EXISTS ON (n:Student) ASSERT n.studentId IS UNIQUE;
MERGE (p:Permission {role: "admin"})
SET
    p.canAccessAdminPanel = true,
    p.canAssignRole = true,
    p.canAssignCourse = true,
    p.canCreateJob = true,
    p.canApproveRelationship = true,
    p.canForkAllCourseBranch = true,
    p.canReadAllCourseBranch = true,
    p.canWriteAllCourseResources = true,
    p.canAccessDLTCPanel = true,
    p.canCreateCourse = true,
    p.canUploadPhoto = true,
    p.canForkTrunk = true,
    p.canReadTrunk = true,
    p.canUpdateTrunk = true,
    p.canAccessInstructorPanel = true,
    p.canProposeRelationship = true,
    p.canCreateGraphConcept = true,
    p.canBeAssignedCourse = false,
    p.canForkAssignedCourseBranch = false,
    p.canReadAssignedCourseBranch = false,
    p.canWriteAssignedCourseResources = false,
    p.canProposeIssue = true,
    p.canReplyIssue = true;

MERGE (p:Permission {role: "DLTC"})
SET
    p.canAccessAdminPanel = false,
    p.canAssignRole = false,
    p.canAssignCourse = false,
    p.canCreateJob = false,
    p.canApproveRelationship = false,
    p.canForkAllCourseBranch = false,
    p.canReadAllCourseBranch = false,
    p.canWriteAllCourseResources = false,
    p.canAccessDLTCPanel = true,
    p.canCreateCourse = true,
    p.canUploadPhoto = true,
    p.canForkTrunk = true,
    p.canReadTrunk = true,
    p.canUpdateTrunk = true,
    p.canAccessInstructorPanel = false,
    p.canProposeRelationship = false,
    p.canCreateGraphConcept = false,
    p.canBeAssignedCourse = false,
    p.canForkAssignedCourseBranch = false,
    p.canReadAssignedCourseBranch = false,
    p.canWriteAssignedCourseResources = false,
    p.canProposeIssue = true,
    p.canReplyIssue = true;

MERGE (p:Permission {role: "instrcutor"})
SET
    p.canAccessAdminPanel = false,
    p.canAssignRole = false,
    p.canAssignCourse = false,
    p.canCreateJob = false,
    p.canApproveRelationship = false,
    p.canForkAllCourseBranch = false,
    p.canReadAllCourseBranch = false,
    p.canWriteAllCourseResources = false,
    p.canAccessDLTCPanel = false,
    p.canCreateCourse = false,
    p.canUploadPhoto = false,
    p.canForkTrunk = false,
    p.canReadTrunk = false,
    p.canUpdateTrunk = false,
    p.canAccessInstructorPanel = true,
    p.canProposeRelationship = true,
    p.canCreateGraphConcept = true,
    p.canBeAssignedCourse = true,
    p.canForkAssignedCourseBranch = true,
    p.canReadAssignedCourseBranch = true,
    p.canWriteAssignedCourseResources = true,
    p.canProposeIssue = true,
    p.canReplyIssue = true;

MERGE (p:Permission {role: "restricted"})
SET
    p.canAccessAdminPanel = false,
    p.canAssignRole = false,
    p.canAssignCourse = false,
    p.canCreateJob = false,
    p.canApproveRelationship = false,
    p.canForkAllCourseBranch = false,
    p.canReadAllCourseBranch = false,
    p.canWriteAllCourseResources = false,
    p.canAccessDLTCPanel = false,
    p.canCreateCourse = false,
    p.canUploadPhoto = false,
    p.canForkTrunk = false,
    p.canReadTrunk = false,
    p.canUpdateTrunk = false,
    p.canAccessInstructorPanel = false,
    p.canProposeRelationship = false,
    p.canCreateGraphConcept = false,
    p.canBeAssignedCourse = false,
    p.canForkAssignedCourseBranch = false,
    p.canReadAssignedCourseBranch = false,
    p.canWriteAssignedCourseResources = false,
    p.canProposeIssue = false,
    p.canReplyIssue = false