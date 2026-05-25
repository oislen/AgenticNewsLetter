import os

from aws_cdk import (
    Stack,
    aws_events as events,
    aws_events_targets as targets,
    aws_iam as iam,
    aws_codebuild as codebuild,
    aws_lambda_event_sources as lambda_events,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
)
from constructs import Construct

from aws.cdk.stacks.constructs import (
    SqsQueueWithDlq,
    EcrRepository,
    LambdaFunction,
    SnsTopic,
    EventBridgeRule,
)

class NewsletterStack(Stack):
    
    def __init__(self, scope: Construct, construct_id: str, initial_run: bool = False, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        #ECR Repository for our Docker Image
        self.ecr_repository = EcrRepository(
            self,
            construct_id="EcrRepository",
            repo_name="ds-newsletter-agent",
            tags={},
        )
        
        # CodeBuild project to build and push Docker image to ECR
        source = codebuild.Source.git_hub(
            owner="oislen",
            repo="AgenticNewsLetter",
            branch_or_ref="main",
            webhook=False,
        )
        
        # SNS Topic (Dispatcher)
        self.sns_topic = SnsTopic(
            self,
            construct_id="SnsTopic",
            topic_name="NewsletterTopic",
            display_name="NewsletterTopic",
            tags={},
        )
        
        # SQS Queue (Processing Queue)
        self.queue = SqsQueueWithDlq(
            self,
            construct_id="ProcessingQueue",
            queue_name="ProcessingQueue",
            dead_letter_queue_name="ProcessingQueueDlq",
            fifo=False,
            retention_period_days=1,
            max_receive_count=3,
            visibility_timeout_seconds=60,
            is_production=False,
            tags={},
        )
        # create filter policy for SNS subscription based on queue configs
        filter_policy = {
            "subject": sns.FilterOrPolicy.filter(
                sns.SubscriptionFilter.string_filter(allowlist=["AgenticNewsLetter"])
            ),
            "status": sns.FilterOrPolicy.filter(
                sns.SubscriptionFilter.string_filter(allowlist=["Start"])
            )
        }
        # connect the SQS queue to the SNS topic for alerts related to this queue
        self.sns_topic.topic.add_subscription(
            subs.SqsSubscription(
                self.queue.queue,
                filter_policy_with_message_body=filter_policy
            )
        )
        
        #self.sns_topic.add_sqs_subscription(self.queue.queue)
        if not initial_run:
            # Lambda Function (The Agent)
            self.agent_lambda = LambdaFunction(
                self,
                construct_id=f"AgentLambda",
                function_name="AgentLambda",
                repository=self.ecr_repository.repository,
                image_tag="latest",
                entrypoint=["/bin/sh", "/home/ubuntu/AgenticNewsLetter/newsletter/entry.sh"],
                cmd=["LambdaHandler.lambda_handler"],
                working_directory="/home/ubuntu/AgenticNewsLetter/newsletter",
                environment={
                    #"AWS_REGION":os.environ["AWS_REGION"],
                    "AWS_ACCOUNT_ID":os.environ["AWS_ACCOUNT_ID"],
                    "TAVILY_API_KEY_ARN":os.environ["TAVILY_API_KEY_ARN"],
                    "SENDER_EMAIL":os.environ["SENDER_EMAIL"],
                    "SENDER_PASSWORD_ARN":os.environ["SENDER_PASSWORD_ARN"],
                    "RECEIVER_EMAIL":os.environ["RECEIVER_EMAIL"],
                    "BEDROCK_MODEL_ID":os.environ["BEDROCK_MODEL_ID"],
                },
                role=None,
                vpc_id=None,
                security_group_ids=None,
                timeout_seconds=120,
                memory_size_mb=1024,
                tags={},
            )
            # allow Lambda to read and call Bedrock
            self.agent_lambda.function.add_to_role_policy(iam.PolicyStatement(
                actions=["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream"],
                resources=["*"] # Narrow this down to specific model ARNs in production
            ))
            # allow Lambda to read the necessary secrets from Secrets Manager
            self.agent_lambda.function.add_to_role_policy(iam.PolicyStatement(
                actions=["secretsmanager:GetSecretValue"],
                resources=[
                    os.environ["TAVILY_API_KEY_ARN"],
                    os.environ["SENDER_PASSWORD_ARN"]
                ]
            ))
            # add sqs trigger to lambda
            self.agent_lambda.function.add_event_source(
                lambda_events.SqsEventSource(
                    self.queue.queue,
                    batch_size=1,
                    enabled=True,
                )
            )
        
        # EventBridge Cron Job (Every Monday 8 AM)
        self.weekly_rule = EventBridgeRule(
            self,
            construct_id="WeeklySchedule",
            rule_name="WeeklySchedule",
            schedule=events.Schedule.cron(minute="0", hour="8", month="*", year="*", week_day="MON"),
            enabled=True,
        )
        # define the message attributes to send to topic
        message = events.RuleTargetInput.from_object({"subject":"AgenticNewsLetter", "status": "Start"})
        # link sns topic to event bridge rule with message attributes
        self.weekly_rule.rule.add_target(targets.SnsTopic(self.sns_topic.topic, message=message))