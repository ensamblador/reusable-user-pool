from aws_cdk import (
    aws_iam as iam,
    Stack,
    Duration,
    aws_cognito as cognito,
    RemovalPolicy,
    CfnOutput,
)
import urllib.parse

from constructs import Construct


class UserPool(Construct):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        stk = Stack.of(self)
        region = stk.region

        self.user_pool = cognito.UserPool(
            self,
            "user_pool",
            account_recovery=cognito.AccountRecovery.EMAIL_ONLY,
            password_policy=cognito.PasswordPolicy(min_length=8),
            self_sign_up_enabled=False,
            removal_policy= RemovalPolicy.DESTROY,
            auto_verify=cognito.AutoVerifiedAttrs(email=True),
            standard_attributes=cognito.StandardAttributes(
                email=cognito.StandardAttribute(required=True)
            ),
            sign_in_aliases=cognito.SignInAliases(email=True),
        )

        self.pool_id = self.user_pool.user_pool_id
        
        

        cognito_console_url = f"https://{region}.console.aws.amazon.com/cognito/v2/idp/user-pools/{self.pool_id}/users?region={region}"

        CfnOutput(self, "POOL_ID", value=self.pool_id)

  

        CfnOutput(
            self,
            "cognito_console",
            description="Crear usuario aca",
            value=cognito_console_url,
        )

    def add_custom_domain(self, domain_prefix):
        self.user_pool_custom_domain = self.user_pool.add_domain(
            "user-pool-domain",
            cognito_domain=cognito.CognitoDomainOptions(domain_prefix=domain_prefix),
        )

    # TODO Mover esto a la aplicacion
    def add_user_pool_client(self, dns_name):
        self.user_pool_client = cognito.UserPoolClient(
            self,
            "Client",
            user_pool=self.user_pool,
            refresh_token_validity= Duration.days(300),
            access_token_validity= Duration.days(1),
            id_token_validity = Duration.days(1),
            user_pool_client_name="AlbAuth",
            generate_secret=True,
            o_auth=cognito.OAuthSettings(
                callback_urls=[
                    # This is the endpoint where the ALB accepts the
                    # response from Cognito
                    f"https://{dns_name}/oauth2/idpresponse",
                    # This is here to allow a redirect to the login page
                    # after the logout has been completed
                    f"https://{dns_name}",
                ],
                flows=cognito.OAuthFlows(authorization_code_grant=True),
                scopes=[cognito.OAuthScope.OPENID],
            ),
            supported_identity_providers=[
                cognito.UserPoolClientIdentityProvider.COGNITO
            ]
        )
        user_pool_client_cf: cognito.CfnUserPoolClient = self.user_pool_client.node.default_child
        user_pool_client_cf.logout_ur_ls = [
            # This is here to allow a redirect to the login page
            # after the logout has been completed
            f"https://{dns_name}"
        ]
        self.user_pool_full_domain = self.user_pool_custom_domain.base_url()
        redirect_uri = urllib.parse.quote('https://' + dns_name)

        self.user_pool_logout_url = f"{self.user_pool_full_domain}/logout?" \
                                    + f"client_id={self.user_pool_client.user_pool_client_id}&" \
                                    + f"logout_uri={redirect_uri}"
        
        self.user_pool_user_info_url = f"{self.user_pool_full_domain}/oauth2/userInfo"

        CfnOutput(self, "base_url", value=self.user_pool_full_domain )