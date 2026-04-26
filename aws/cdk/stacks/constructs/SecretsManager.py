import logging

from aws_cdk import (
    aws_secretsmanager as secrets
)
from constructs import Construct

class SecretsManager(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        *,
        secret_name: str,
    ) -> None:
        super().__init__(scope, construct_id)

        logging.info(f"Creating SecretsManager for '{secret_name}'")
        # Secret Manager for API Keys and other sensitive information
        self.secrets = secrets.Secret.from_secret_name_v2(
            self,
            id=construct_id,
            secret_name=secret_name
        )
