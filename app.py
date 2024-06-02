#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk.wgse_ng_stack import WGSENGStack


app = cdk.App()
WGSENGStack(app, "WGSENGStack")

app.synth()
