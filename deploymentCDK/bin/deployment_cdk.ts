#!/usr/bin/env node
import * as cdk from "aws-cdk-lib";
import { MiwaStack } from "../lib/miwa_lambda_stack";


const app = new cdk.App();
new MiwaStack(app, "miwa-stack", {
  env: {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region: process.env.CDK_DEFAULT_REGION,
  },
});

cdk.Tags.of(app).add("project", "miwa");
