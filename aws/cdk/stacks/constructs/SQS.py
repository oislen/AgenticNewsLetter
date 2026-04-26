from typing import Optional
import logging

from aws_cdk import (
    Duration,
    Tags,
    aws_sqs as sqs,
)
from constructs import Construct


class SqsQueueWithDlq(Construct):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        *,
        queue_name: str,
        dead_letter_queue_name: str,
        fifo: bool = False,
        retention_period_days: int = 1,
        max_receive_count: int = 3,
        visibility_timeout_seconds: int = 30,
        is_production: bool = False,
        tags: dict,
    ) -> None:
        super().__init__(scope, construct_id)

        logging.info(f"Creating SQS queue '{queue_name}' with dead-letter queue '{dead_letter_queue_name}' for message processing")
        # Dead-letter queue
        self.dlq = sqs.Queue(
            self,
            id=f"{construct_id}Dlq",
            queue_name=dead_letter_queue_name,
            retention_period=Duration.days(retention_period_days),
            encryption=sqs.QueueEncryption.SQS_MANAGED,
            enforce_ssl=True,
            fifo=fifo,
        )

        for key, value in tags.items():
            Tags.of(self.dlq).add(key, value)

        # Main queue
        self.queue = sqs.Queue(
            self,
            id=f"{construct_id}MainQueue",
            queue_name=queue_name,
            visibility_timeout=Duration.seconds(visibility_timeout_seconds),
            dead_letter_queue=sqs.DeadLetterQueue(
                max_receive_count=max_receive_count,
                queue=self.dlq,
            ),
            encryption=sqs.QueueEncryption.SQS_MANAGED,
            enforce_ssl=True,
            fifo=fifo,
        )

        for key, value in tags.items():
            Tags.of(self.queue).add(key, value)

        if is_production:
            logging.info(f"Production env, we should create alarms")
        # create alarms here
        else:
            logging.info(f"Not production, skipping creating alarms")


    @property
    def queue_arn(self) -> str:
        return self.queue.queue_arn

    @property
    def dlq_arn(self) -> str:
        return self.dlq.queue_arn
