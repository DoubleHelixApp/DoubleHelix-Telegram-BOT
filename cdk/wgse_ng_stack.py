from aws_cdk import Stack
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_logs as logs
from aws_cdk import aws_iam
from aws_cdk import aws_secretsmanager as secretsmanager
from constructs import Construct


class WGSENGStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        post_announcement_lambda = _lambda.Function(
            self,
            "PostAnnouncements",
            runtime=_lambda.Runtime.PYTHON_3_11,
            code=_lambda.Code.from_asset("lambda"),
            handler="post_message.handler",
        )

        api = apigateway.LambdaRestApi(
            self,
            "PostAnnouncementApi",
            handler=post_announcement_lambda,
            proxy=False,
            cloud_watch_role=True,
        )
        secret = secretsmanager.Secret.from_secret_name_v2(
            self, "secret", "TelegramBOTAPIKey"
        )
        secret.grant_read(post_announcement_lambda)
        
        post_announcements_resource = api.root.add_resource("postAnnouncement")
        post_announcements_resource.add_method("POST")
