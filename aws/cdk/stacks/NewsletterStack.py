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
    CodeBuildProject,
    EventBridgeRule,
    SecretsManager,
)

class NewsletterStack(Stack):
    
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
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
        
        self.inbound_consumer_build = CodeBuildProject(
            self,
            construct_id="CodeBuildProject",
            project_name="CodeBuildJob",
            source=source,
            ecr_repo=self.ecr_repository.repository,
            image_tag="latest",
            tags={},
            vpc_id=None,
            subnet_ids=None,
            security_group_id=None,
            compute_type=codebuild.ComputeType.MEDIUM,
            notification_topic_arn=None,
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
        
        # SNS Topic (Dispatcher)
        self.sns_topic = SnsTopic(
            self,
            construct_id="SnsTopic",
            topic_name="NewsletterTopic",
            display_name="NewsletterTopic",
            tags={},
        )
        #self.sns_topic.add_sqs_subscription(self.queue.queue)
        
        # Lambda Function (The Agent)
        self.agent_lambda = LambdaFunction(
            self,
            construct_id=f"AgentLambda",
            function_name="AgentLambda",
            repository=self.ecr_repository.repository,
            image_tag="latest",  # same tag CodeBuild pushed
            entrypoint=["sh, /home/ubuntu/entry.sh"],
            cmd=["AgenticNewsLetter.LambdaHandlers.AgenticNewsLetter.lambda_handler"],
            working_directory="/home/ubuntu/",
            environment={},
            role=None,
            vpc_id=None,
            security_group_ids=None,
            timeout_seconds=60,
            memory_size_mb=1024,
            tags={},
        )
        
        # create filter policy for SNS subscription based on queue configs
        filter_policy = {
            "subject": sns.SubscriptionFilter.string_filter(
                allowlist=["AgenticNewsLetter"]
            ),
            "status": sns.SubscriptionFilter.string_filter(
                allowlist=["Start"]
            )
        }
        # connect the SQS queue to the SNS topic for alerts related to this queue
        self.sns_topic.topic.add_subscription(
            subs.SqsSubscription(
                self.queue.queue,
                filter_policy=filter_policy
            )
        )
        
        ## Secret Manager for API Keys
        #self.agent_secrets = SecretsManager(
        #    self,
        #    construct_id="AgentSecrets",
        #    secret_name="ds_newsletter_credentials"
        #)
        
        # Permissions: Allow Lambda to read secrets and call Bedrock
        #self.agent_secrets.secrets.grant_read(self.agent_lambda.function)
        self.agent_lambda.function.add_to_role_policy(iam.PolicyStatement(
            actions=["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream"],
            resources=["*"] # Narrow this down to specific model ARNs in production
        ))
        
        # EventBridge Cron Job (Every Monday 8 AM)
        self.weekly_rule = EventBridgeRule(
            self,
            construct_id="WeeklySchedule",
            rule_name="WeeklySchedule",
            schedule=events.Schedule.cron(minute="0", hour="8", month="*", year="*", week_day="MON"),
        )
        self.weekly_rule.rule.add_target(targets.SnsTopic(self.sns_topic.topic))