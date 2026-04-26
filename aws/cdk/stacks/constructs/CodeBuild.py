import logging
from typing import Optional, List

from aws_cdk import (
    Tags,
    aws_codebuild as codebuild,
    aws_ecr as ecr,
    aws_ec2 as ec2,
    aws_codestarnotifications as codestar,
    aws_sns as sns,
    aws_iam as iam,
)
from constructs import Construct


class CodeBuildProject(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        *,
        project_name: str,
        source: codebuild.ISource,
        ecr_repo: ecr.IRepository,
        image_tag: str,
        tags: dict,
        vpc_id: Optional[str] = None,
        subnet_ids: Optional[List[str]] = None,
        security_group_id: Optional[str] = None,
        compute_type: codebuild.ComputeType = codebuild.ComputeType.SMALL,
        buildspec: Optional[codebuild.BuildSpec] = None,
        notification_topic_arn: Optional[str] = None, 
    ) -> None:
        super().__init__(scope, construct_id)

        logging.info(f"Setting up CodeBuild {project_name} project for Lambda image builds")
        # Environment variables passed into the build
        environment_variables = {
            "IMAGE_REPO_URI": codebuild.BuildEnvironmentVariable(
                value=ecr_repo.repository_uri
            ),
            "IMAGE_TAG": codebuild.BuildEnvironmentVariable(value=image_tag),
        }

        # Use repo-provided buildspec by default
        effective_buildspec = buildspec or codebuild.BuildSpec.from_source_filename(
            "buildspec.yml"
        )

        # Optional network lookups (VPC, subnets, security groups)
        vpc: Optional[ec2.IVpc] = None
        subnets: Optional[list[ec2.ISubnet]] = None
        security_groups: Optional[list[ec2.ISecurityGroup]] = None

        if vpc_id:
            vpc = ec2.Vpc.from_lookup(
                self,
                id="CodeBuildVpc",
                vpc_id=vpc_id,
            )

        if subnet_ids:
            subnets = [
                ec2.Subnet.from_subnet_id(self, f"CodeBuildSubnet{i}", subnet_id)
                for i, subnet_id in enumerate(subnet_ids, start=1)
            ]

        if security_group_id:
            security_groups = [
                ec2.SecurityGroup.from_security_group_id(
                    self,
                    "CodeBuildSecurityGroup",
                    security_group_id=security_group_id,
                )
            ]

        self.project = codebuild.Project(
            self,
            id=construct_id,
            project_name=project_name,
            source=source,
            environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.AMAZON_LINUX_2_5,
                compute_type=compute_type,
                privileged=True,
            ),
            environment_variables=environment_variables,
            build_spec=effective_buildspec,
            vpc=vpc,
            subnet_selection=ec2.SubnetSelection(subnets=subnets) if subnets else None,
            security_groups=security_groups,
        )

        # Build Failure Notifications to Slack via SNS + Chatbot
        if notification_topic_arn:
            topic = sns.Topic.from_topic_arn(
                self,
                "CodeBuildNotificationsTopic",
                notification_topic_arn,
            )

            failure_rule_name = f"BuildFailureRule"

            codestar.NotificationRule(
                self,
                failure_rule_name,
                detail_type=codestar.DetailType.FULL,
                events=[
                    "codebuild-project-build-state-failed"
                ],
                source=self.project,
                targets=[topic],
            )

        # Grant ECR push/pull permissions
        ecr_repo.grant_pull_push(self.project.role)

        # Additional permissions: logs, S3 (for artifacts), SSM, KMS
        self.project.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "CloudWatchLogsFullAccess"
            )
        )
        self.project.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonS3FullAccess"
            )
        )
        self.project.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonSSMReadOnlyAccess"
            )
        )
        self.project.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "AWSKeyManagementServicePowerUser"
            )
        )

        # Tag the project
        for key, value in tags.items():
            Tags.of(self.project).add(key, value)


    @property
    def codebuild_project(self) -> codebuild.IProject:
        return self.project
