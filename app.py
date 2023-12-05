#!/usr/bin/env python3
import os
import boto3

import aws_cdk as cdk

from user_pool.user_pool_stack import UserPoolStack
TAGS = {"app": "generative ai business apps", "customer": "vpc-stack"}
region = os.environ.get("AWS_DEFAULT_REGION")
if not region: region = "us-east-1"

caller = boto3.client('sts').get_caller_identity()
account_id = caller.get("Account")

app = cdk.App()
stk = UserPoolStack(app, "user-pool-stack",     env=cdk.Environment(account=account_id, region=region))

if TAGS.keys():
    for k in TAGS.keys():
        cdk.Tags.of(stk).add(k, TAGS[k])
app.synth()
