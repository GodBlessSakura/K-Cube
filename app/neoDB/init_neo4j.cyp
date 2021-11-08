CREATE CONSTRAINT user_uid_constraint IF NOT EXISTS ON (n:User) ASSERT n.userId IS UNIQUE;
CREATE CONSTRAINT user_email_constraint IF NOT EXISTS ON (n:User) ASSERT n.email IS UNIQUE;
CREATE CONSTRAINT permission_uid_constraint IF NOT EXISTS ON (n:Permission) ASSERT n.role IS UNIQUE;
CREATE CONSTRAINT deltaGraph_uid_constraint IF NOT EXISTS ON (n:DeltaGraph) ASSERT n.deltaGraphId IS UNIQUE;
CREATE CONSTRAINT trunkCache_uid_constraint IF NOT EXISTS ON (n:Trunk) ASSERT n.cachedGraphId IS UNIQUE;
CREATE CONSTRAINT course_uid_constraint IF NOT EXISTS ON (n:Course) ASSERT n.displayName IS UNIQUE;
CREATE CONSTRAINT GraphConcept_uid_constraint IF NOT EXISTS ON (n:GraphConcept) ASSERT n.name IS UNIQUE;
CREATE CONSTRAINT GraphRelationship_uid_constraint IF NOT EXISTS ON (n:GraphRelationship) ASSERT n.name IS UNIQUE;
CREATE CONSTRAINT job_uid_constraint IF NOT EXISTS ON (n:Job) ASSERT n.jobId IS UNIQUE;
CREATE CONSTRAINT student_uid_constraint IF NOT EXISTS ON (n:Student) ASSERT n.studentId IS UNIQUE;
MERGE (p:Permission {role: "admin"})
SET
    p = {
        role: "admin",
        canAccessAdminPanel : true,
        canAssignRole : true,
        canAssignCourse : true,
        canCreateJob : true,
        canApproveRelationship : true,
        canForkAllCourseBranch : true,
        canReadAllCourseBranch : true,
        canWriteAllCourseResources : true,
        canAccessDLTCPanel : true,
        canCreateCourse : true,
        canUploadPhoto : true,
        canForkTrunk : true,
        canReadTrunk : true,
        canUpdateTrunk : true,
        canAccessInstructorPanel : true,
        canProposeRelationship : true,
        canCreateGraphConcept : true,
        canBeAssignedCourse : false,
        canForkAssignedCourseBranch : false,
        canReadAssignedCourseBranch : false,
        canWriteAssignedCourseResources : false,
        canGiveFeedback : true,
        canReplyFeedback : true
    };

MERGE (p:Permission {role: "DLTC"})
SET
    p = {
        role: "DLTC",
        canAccessAdminPanel : false,
        canAssignRole : false,
        canAssignCourse : false,
        canCreateJob : false,
        canApproveRelationship : false,
        canForkAllCourseBranch : false,
        canReadAllCourseBranch : false,
        canWriteAllCourseResources : false,
        canAccessDLTCPanel : true,
        canCreateCourse : true,
        canUploadPhoto : true,
        canForkTrunk : true,
        canReadTrunk : true,
        canUpdateTrunk : true,
        canAccessInstructorPanel : false,
        canProposeRelationship : false,
        canCreateGraphConcept : false,
        canBeAssignedCourse : false,
        canForkAssignedCourseBranch : false,
        canReadAssignedCourseBranch : false,
        canWriteAssignedCourseResources : false,
        canGiveFeedback : true,
        canReplyFeedback : true
    };

MERGE (p:Permission {role: "instructor"})
SET
    p = {
        role: "instructor",
        canAccessAdminPanel : false,
        canAssignRole : false,
        canAssignCourse : false,
        canCreateJob : false,
        canApproveRelationship : false,
        canForkAllCourseBranch : false,
        canReadAllCourseBranch : false,
        canWriteAllCourseResources : false,
        canAccessDLTCPanel : false,
        canCreateCourse : false,
        canUploadPhoto : false,
        canForkTrunk : false,
        canReadTrunk : false,
        canUpdateTrunk : false,
        canAccessInstructorPanel : true,
        canProposeRelationship : true,
        canCreateGraphConcept : true,
        canBeAssignedCourse : true,
        canForkAssignedCourseBranch : true,
        canReadAssignedCourseBranch : true,
        canWriteAssignedCourseResources : true,
        canGiveFeedback : true,
        canReplyFeedback : true
    };

MERGE (p:Permission {role: "student"})
SET
    p = {
        role: "student",
        canAccessAdminPanel : false,
        canAssignRole : false,
        canAssignCourse : false,
        canCreateJob : false,
        canApproveRelationship : false,
        canForkAllCourseBranch : false,
        canReadAllCourseBranch : false,
        canWriteAllCourseResources : false,
        canAccessDLTCPanel : false,
        canCreateCourse : false,
        canUploadPhoto : false,
        canForkTrunk : false,
        canReadTrunk : false,
        canUpdateTrunk : false,
        canAccessInstructorPanel : true,
        canProposeRelationship : true,
        canCreateGraphConcept : true,
        canBeAssignedCourse : true,
        canForkAssignedCourseBranch : true,
        canReadAssignedCourseBranch : true,
        canWriteAssignedCourseResources : true,
        canGiveFeedback : true,
        canReplyFeedback : true
    };

MERGE (p:Permission {role: "restricted"})
SET
    p = {
        role: "restricted",
        canAccessAdminPanel : false,
        canAssignRole : false,
        canAssignCourse : false,
        canCreateJob : false,
        canApproveRelationship : false,
        canForkAllCourseBranch : false,
        canReadAllCourseBranch : false,
        canWriteAllCourseResources : false,
        canAccessDLTCPanel : false,
        canCreateCourse : false,
        canUploadPhoto : false,
        canForkTrunk : false,
        canReadTrunk : false,
        canUpdateTrunk : false,
        canAccessInstructorPanel : false,
        canProposeRelationship : false,
        canCreateGraphConcept : false,
        canBeAssignedCourse : false,
        canForkAssignedCourseBranch : false,
        canReadAssignedCourseBranch : false,
        canWriteAssignedCourseResources : false,
        canGiveFeedback : false,
        canReplyFeedback : false
    }