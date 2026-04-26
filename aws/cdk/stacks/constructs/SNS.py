import logging

from aws_cdk import (
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    Tags,
)
from constructs import Construct

class SnsTopic(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        *,
        topic_name: str,
        display_name: str = None,
        fifo: bool = False,
        tags: dict = None,
    ) -> None:
        super().__init__(scope, construct_id)

        logging.info(f"Creating SNS topic '{topic_name}' for dispatching messages to SQS")
        self.topic = sns.Topic(
            self,
            id=construct_id,
            topic_name=topic_name,
            display_name=display_name,
            fifo=fifo,
            content_based_deduplication=True if fifo else None,
        )

        if tags:
            for key, value in tags.items():
                Tags.of(self.topic).add(key, value)

    def add_sqs_subscription(self, queue):
        """Helper method to subscribe an SQS queue to this topic"""
        self.topic.add_subscription(subs.SqsSubscription(queue))