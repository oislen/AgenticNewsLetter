import logging

from aws_cdk import (
    aws_events as events
)
from constructs import Construct

class EventBridgeRule(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        *,
        rule_name: str,
        schedule: events.Schedule,
    ) -> None:
        super().__init__(scope, construct_id)

        logging.info(f"Creating EventBridge rule '{rule_name}'")
        self.rule = events.Rule(
            self, 
            id=construct_id,
            rule_name=rule_name,
            schedule=schedule,
        )
