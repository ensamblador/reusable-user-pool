from aws_cdk import Stack, aws_ssm as ssm, aws_cognito as cognito, CfnParameter, Fn, CfnOutput

from constructs import Construct
from cognito_stack import UserPool


class UserPoolStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.create_user_pool()


        hosted_zone_domain_name = self.get_ssm_parameter("hosted-zone-domain-name")
        dns_prefix = hosted_zone_domain_name.replace(".", "-")
        self.users.add_custom_domain(domain_prefix=dns_prefix)
    
        user_cfnparam = CfnParameter(self, "users", type= 'AWS::SSM::Parameter::Value<List<String>>', default="/gen-ai-apps/create-users").value_as_list
        user0 = Fn.select(0,user_cfnparam)
        user_pool0 = self.create_user(user0)
        CfnOutput(self, "username-0", value=user_pool0.username )


        self.create_ssm_param("pool-id", self.users.pool_id)
        self.create_ssm_param("app-user-pool-custom-domain", self.users.user_pool_custom_domain.domain_name)


    def create_user(self, email):
        #TODO add emails by parameter store
        user_pool0 = cognito.CfnUserPoolUser(self, "user0",
            user_pool_id=self.users.pool_id,
            desired_delivery_mediums= ["EMAIL"],
            #user_attributes=[cognito.CfnUserPoolUser.AttributeTypeProperty(name="email",value=email)],
            username=email
        )
        return user_pool0
        




    def create_user_pool(self):
        self.users = UserPool(self, "Users")

    def create_ssm_param(self, name, value):
        ssm.StringParameter(
            self,
            f"ssm-{name}",
            parameter_name=f"/gen-ai-apps/{name}",
            string_value=value,
        )

    def get_ssm_parameter(self, parameter_name):
        return ssm.StringParameter.value_from_lookup(
            self, parameter_name=f"/gen-ai-apps/{parameter_name}"
        )

