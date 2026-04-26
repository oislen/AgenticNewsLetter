import logging
from typing import Dict, List, Optional

from aws_cdk import (
    Duration,
    Tags,
    aws_ec2 as ec2,
    aws_ecr as ecr,
    aws_iam as iam,
    aws_lambda as _lambda,
)
from constructs import Construct


class LambdaFunction(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        *,
        function_name: str,
        repository: ecr.IRepository,
        image_tag: str,
        entrypoint: Optional[List[str]] = None,
        cmd: Optional[List[str]] = None,
        working_directory: Optional[str] = None,
        environment: Optional[Dict[str, str]] = None,
        timeout_seconds: int = 30,
        memory_size_mb: int = 256,
        role: Optional[iam.IRole] = None,
        vpc: Optional[ec2.IVpc] = None,
        security_groups: Optional[List[ec2.ISecurityGroup]] = None,
        vpc_id: Optional[str] = None,
        security_group_ids: Optional[List[str]] = None,
        tags: Dict[str, str],
    ) -> None:
        super().__init__(scope, construct_id)

        logging.info(f"Creating Lambda {function_name} function for the agent")
        # Optional network lookups if IDs are provided and concrete objects are not
        if vpc is None and vpc_id is not None:
            vpc = ec2.Vpc.from_lookup(
                self,
                "LambdaVpc",
                vpc_id=vpc_id,
            )

        if security_groups is None and security_group_ids:
            security_groups = [
                ec2.SecurityGroup.from_security_group_id(
                    self,
                    id=f"LambdaSecurityGroup{i}",
                    security_group_id=sg_id,
                )
                for i, sg_id in enumerate(security_group_ids, start=1)
            ]

        #existing_repo = ecr.Repository.from_repository_name(
        #    self, 
        #    "ExistingEcrRepo", 
        #    repository_name=ecr_repo_name
        #)
        self.function = _lambda.DockerImageFunction(
            self,
            id=construct_id,
            code=_lambda.DockerImageCode.from_ecr(
                repository=repository,
                tag_or_digest=image_tag,
                entrypoint=entrypoint,
                cmd=cmd,
                working_directory=working_directory,
            ),
            function_name=function_name,
            role=role,
            vpc=vpc,
            security_groups=security_groups,
            environment=environment or {},
            timeout=Duration.seconds(timeout_seconds),
            memory_size=memory_size_mb,
        )

        # Apply standard tags
        for key, value in tags.items():
            Tags.of(self.function).add(key, value)
