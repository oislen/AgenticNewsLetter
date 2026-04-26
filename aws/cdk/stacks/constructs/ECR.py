import logging
from aws_cdk import (
    Tags,
    aws_ecr as ecr,
)
from constructs import Construct

class EcrRepository(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        *,
        repo_name: str,
        tags: dict,
    ) -> None:
        super().__init__(scope, construct_id)

        logging.info(f"Initializing ECR Repository {repo_name}")
        # Create ECR repository with best practices (encryption, scanning, lifecycle rules)
        self.repository = ecr.Repository(
            self,
            id=construct_id,
            repository_name=repo_name,
            image_scan_on_push=True,
            image_tag_mutability=ecr.TagMutability.MUTABLE,
            encryption=ecr.RepositoryEncryption.AES_256,
            lifecycle_rules=[
                ecr.LifecycleRule(
                    max_image_count=10
                )
            ],
        )
        # Add tags to the repository
        for key, value in tags.items():
            Tags.of(self.repository).add(key, value)

    @property
    def get_repository_uri(self) -> str:
        return self.repository.repository_uri
