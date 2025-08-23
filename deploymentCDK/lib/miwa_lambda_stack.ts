import { PythonFunction } from "@aws-cdk/aws-lambda-python-alpha";
import * as cdk from "aws-cdk-lib";
import { Duration, RemovalPolicy } from "aws-cdk-lib";
import * as apigw from "aws-cdk-lib/aws-apigateway";
import { Code, Function, Runtime } from "aws-cdk-lib/aws-lambda";
import { Construct } from "constructs";
import * as path from "path";

// import * as sqs from 'aws-cdk-lib/aws-sqs';

export class MiwaStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const lambdaFn = new PythonFunction(this, "miwa-greeter-lambda", {
      entry: path.join(__dirname, "..", "lambda"),
      runtime: Runtime.PYTHON_3_11,
      index: "handler.py",
      handler: "lambda_handler",
      timeout: Duration.seconds(30),
      memorySize: 256,
      environment: {
        SENDGRID_API_KEY: process.env.SENDGRID_API_KEY || "",
        SENDGRID_SENDER: process.env.SENDER || "",
      },
    });

    const api = new apigw.LambdaRestApi(this, "miwa-api", {
      handler: lambdaFn,
      proxy: false,
    });
    new cdk.CfnOutput(this, "root-endpoint", {
      value: api.url || "Something went wrong with the deploy",
    });

    // integración Lambda
    const integration = new apigw.LambdaIntegration(lambdaFn);

    // crea recurso /send y método POST
    const send = api.root.addResource("send");
    send.addMethod("POST", integration); // ← ahora el API tiene un método

    new cdk.CfnOutput(this, "APIEndpoint", { value: api.url! + "send" });
    // The code that defines your stack goes here

    // example resource
    // const queue = new sqs.Queue(this, "DeploymentCdkQueue", {
    //   visibilityTimeout: cdk.Duration.seconds(300)
    // });
  }
}
