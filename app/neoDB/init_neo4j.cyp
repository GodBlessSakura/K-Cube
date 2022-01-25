CREATE CONSTRAINT user_uid_constraint IF NOT EXISTS ON (n:User) ASSERT n.userId IS UNIQUE;
CREATE CONSTRAINT user_email_constraint IF NOT EXISTS ON (n:User) ASSERT n.email IS UNIQUE;
CREATE CONSTRAINT permission_uid_constraint IF NOT EXISTS ON (n:Permission) ASSERT n.role IS UNIQUE;
CREATE CONSTRAINT deltaGraph_uid_constraint IF NOT EXISTS ON (n:DeltaGraph) ASSERT n.deltaGraphId IS UNIQUE;
CREATE CONSTRAINT course_uid_constraint IF NOT EXISTS ON (n:Course) ASSERT n.courseName IS UNIQUE;
CREATE CONSTRAINT GraphConcept_uid_constraint IF NOT EXISTS ON (n:GraphConcept) ASSERT n.name IS UNIQUE;
CREATE CONSTRAINT GraphRelationship_uid_constraint IF NOT EXISTS ON (n:GraphRelationship) ASSERT n.name IS UNIQUE;
CREATE CONSTRAINT job_uid_constraint IF NOT EXISTS ON (n:Job) ASSERT n.jobId IS UNIQUE;
CREATE CONSTRAINT student_uid_constraint IF NOT EXISTS ON (n:Student) ASSERT n.studentId IS UNIQUE;
CREATE CONSTRAINT MetaConcept_uid_constraint IF NOT EXISTS ON (n:MetaConcept) ASSERT n.name IS UNIQUE;
MERGE (p:Permission {role: "admin"})
SET
    p = {
        role: "admin",
        canAssignRole : true,
        canCreateJob : true,
        canApproveRelationship : true,
        canWriteAllCourseBranch : true,
        canReadAllCourseBranch : true,
        canWriteAllCourseMaterial : true,
        canViewInternalCourse : true,
        canSetInternalCourse : true,
        canCreateCourse : true,
        canUploadPhoto : true,
        canWriteTrunk : true,
        canReadTrunk : true,
        canUpdateTrunk : true,
        canProposeRelationship : true,
        canCreateGraphConcept : true,
        canJoinCourse : false,
        canWriteTeachingCourseBranch : true,
        canReadTeachingCourseBranch : true,
        canWriteTeachingCourseMaterial : false,
        canGiveFeedback : true,
        canReplyFeedback : true
    };

MERGE (p:Permission {role: "DLTC"})
SET
    p = {
        role: "DLTC",
        canAssignRole : false,
        canCreateJob : false,
        canApproveRelationship : false,
        canWriteAllCourseBranch : false,
        canReadAllCourseBranch : false,
        canWriteAllCourseMaterial : false,
        canViewInternalCourse : true,
        canSetInternalCourse : true,
        canCreateCourse : false,
        canUploadPhoto : false,
        canWriteTrunk : true,
        canReadTrunk : true,
        canUpdateTrunk : true,
        canProposeRelationship : false,
        canCreateGraphConcept : false,
        canJoinCourse : false,
        canWriteTeachingCourseBranch : false,
        canReadTeachingCourseBranch : false,
        canWriteTeachingCourseMaterial : false,
        canGiveFeedback : true,
        canReplyFeedback : true
    };

MERGE (p:Permission {role: "instructor"})
SET
    p = {
        role: "instructor",
        canAssignRole : false,
        canCreateJob : false,
        canApproveRelationship : false,
        canWriteAllCourseBranch : false,
        canReadAllCourseBranch : false,
        canWriteAllCourseMaterial : false,
        canViewInternalCourse : true,
        canSetInternalCourse : false,
        canCreateCourse : true,
        canUploadPhoto : true,
        canWriteTrunk : false,
        canReadTrunk : true,
        canUpdateTrunk : false,
        canProposeRelationship : true,
        canCreateGraphConcept : true,
        canJoinCourse : true,
        canWriteTeachingCourseBranch : true,
        canReadTeachingCourseBranch : true,
        canWriteTeachingCourseMaterial : true,
        canGiveFeedback : true,
        canReplyFeedback : true
    };

MERGE (p:Permission {role: "student"})
SET
    p = {
        role: "student",
        canAssignRole : false,
        canCreateJob : false,
        canApproveRelationship : false,
        canWriteAllCourseBranch : false,
        canReadAllCourseBranch : false,
        canWriteAllCourseMaterial : false,
        canViewInternalCourse : false,
        canSetInternalCourse : false,
        canCreateCourse : false,
        canUploadPhoto : false,
        canWriteTrunk : false,
        canReadTrunk : false,
        canUpdateTrunk : false,
        canProposeRelationship : false,
        canCreateGraphConcept : false,
        canJoinCourse : false,
        canWriteTeachingCourseBranch : false,
        canReadTeachingCourseBranch : false,
        canWriteTeachingCourseMaterial : false,
        canGiveFeedback : true,
        canReplyFeedback : true
    };

MERGE (p:Permission {role: "restricted"})
SET
    p = {
        role: "restricted",
        canAssignRole : false,
        canCreateJob : false,
        canApproveRelationship : false,
        canWriteAllCourseBranch : false,
        canReadAllCourseBranch : false,
        canWriteAllCourseMaterial : false,
        canViewInternalCourse : false,
        canSetInternalCourse : false,
        canCreateCourse : false,
        canUploadPhoto : false,
        canWriteTrunk : false,
        canReadTrunk : false,
        canUpdateTrunk : false,
        canProposeRelationship : false,
        canCreateGraphConcept : false,
        canJoinCourse : false,
        canWriteTeachingCourseBranch : false,
        canReadTeachingCourseBranch : false,
        canWriteTeachingCourseMaterial : false,
        canGiveFeedback : false,
        canReplyFeedback : false
    }