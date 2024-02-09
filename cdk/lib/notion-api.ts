/** @format */

import {
  Stack,
  StackProps,
  Duration,
  RemovalPolicy,
  aws_lambda as lambda,
  aws_iam as iam,
  aws_apigateway as apigateway,
  aws_events as events,
  aws_events_targets as targets,
  aws_s3 as s3,
} from "aws-cdk-lib";
import { Construct } from "constructs";

// CONFIG
const RUNTIME = lambda.Runtime.PYTHON_3_11;
const TIMEOUT = 30;
const APP_DIR_PATH = "../notion_api";
const LAYER_ZIP_PATH = "../dependencies.zip";

export class NotionApi extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    // S3バケットを作成
    const bucket = new s3.Bucket(this, "NotionApiBucket", {
      bucketName: "notion-api-bucket-koboriakira",
      removalPolicy: RemovalPolicy.DESTROY,
    });

    const role = this.makeRole(bucket.bucketArn);
    const myLayer = this.makeLayer();
    const fn = this.createLambdaFunction(
      "Lambda",
      "main.handler",
      role,
      myLayer
    );
    this.makeApiGateway(fn);

    this.createEventLambda(
      "create_daily_log",
      role,
      myLayer,
      // 毎週月曜日10:00に実行
      events.Schedule.cron({
        minute: "0",
        hour: "1",
        month: "*",
        year: "*",
        weekDay: "MON",
      })
    );

    this.createEventLambda(
      "clean_empty_title_page",
      role,
      myLayer,
      // 10分ごとに実行
      events.Schedule.cron({
        minute: "*/10",
        hour: "*",
        month: "*",
        year: "*",
        weekDay: "*",
      })
    );

    this.createEventLambda(
      "collect_updated_pages",
      role,
      myLayer,
      // 毎日22時に実行
      events.Schedule.cron({
        minute: "0",
        hour: "13",
        month: "*",
        year: "*",
        weekDay: "*",
      })
    );

    this.createEventLambda(
      "postpone_task",
      role,
      myLayer,
      // 毎日2時に実行
      events.Schedule.cron({
        minute: "0",
        hour: "17",
        month: "*",
        year: "*",
        weekDay: "*",
      })
    );

    this.createEventLambda(
      "update_current_tasks",
      role,
      myLayer,
      // 3分ごとに実行(8時から24時まで)
      events.Schedule.cron({
        minute: "*/3",
        hour: "23-15",
        month: "*",
        year: "*",
        weekDay: "*",
      })
    );
  }

  createEventLambda(
    handlerName: string,
    role: iam.Role,
    myLayer: lambda.LayerVersion,
    schedule: events.Schedule
  ): lambda.Function {
    // スネークケースであるhandler_nameをキャメルケースに変換
    const resourceName = handlerName
      .split("_")
      .map((word, index) =>
        index === 0 ? word : word.charAt(0).toUpperCase() + word.slice(1)
      )
      .join("");

    const fn = this.createLambdaFunction(
      resourceName,
      `${handlerName}.handler`,
      role,
      myLayer,
      false
    );
    new events.Rule(this, `${resourceName}Rule`, {
      schedule: schedule,
      targets: [new targets.LambdaFunction(fn, { retryAttempts: 0 })],
    });
    return fn;
  }

  /**
   * Create or retrieve an IAM role for the Lambda function.
   * @returns {iam.Role} The created or retrieved IAM role.
   */
  makeRole(bucketArn: string) {
    // Lambdaの実行ロールを取得または新規作成
    const role = new iam.Role(this, "LambdaRole", {
      assumedBy: new iam.ServicePrincipal("lambda.amazonaws.com"),
    });

    // Lambda の実行ロールに管理ポリシーを追加
    role.addManagedPolicy(
      iam.ManagedPolicy.fromAwsManagedPolicyName(
        "service-role/AWSLambdaBasicExecutionRole"
      )
    );

    // 必要に応じて追加の権限をポリシーとしてロールに付与
    role.addToPrincipalPolicy(
      new iam.PolicyStatement({
        actions: ["lambda:InvokeFunction", "lambda:InvokeAsync"],
        resources: ["*"],
      })
    );
    role.addToPrincipalPolicy(
      new iam.PolicyStatement({
        actions: ["s3:*"],
        resources: [bucketArn, bucketArn + "/*"],
      })
    );

    return role;
  }

  /**
   * Create or retrieve a Lambda layer.
   * @returns {lambda.LayerVersion} The created or retrieved Lambda layer.
   */
  makeLayer() {
    return new lambda.LayerVersion(this, "Layer", {
      code: lambda.Code.fromAsset(LAYER_ZIP_PATH), // レイヤーの内容を含むディレクトリ
      compatibleRuntimes: [RUNTIME], // このレイヤーが互換性を持つランタイム
    });
  }

  /**
   * Create a Lambda function.
   * @param {iam.Role} role The IAM role for the Lambda function.
   * @param {lambda.LayerVersion} myLayer The Lambda layer to be used.
   * @returns {lambda.Function} The created Lambda function.
   */
  createLambdaFunction(
    name: string,
    handler_name: string,
    role: iam.Role,
    myLayer: lambda.LayerVersion,
    function_url_enabled: boolean = false
  ): lambda.Function {
    const fn = new lambda.Function(this, name, {
      runtime: RUNTIME,
      handler: handler_name,
      code: lambda.Code.fromAsset(APP_DIR_PATH),
      role: role,
      layers: [myLayer],
      timeout: Duration.seconds(TIMEOUT),
    });

    fn.addEnvironment("NOTION_SECRET", process.env.NOTION_SECRET || "");
    fn.addEnvironment(
      "UNSPLASH_ACCESS_KEY",
      process.env.UNSPLASH_ACCESS_KEY || ""
    );
    fn.addEnvironment("SLACK_BOT_TOKEN", process.env.SLACK_BOT_TOKEN || "");
    fn.addEnvironment("SLACK_USER_TOKEN", process.env.SLACK_USER_TOKEN || "");

    if (function_url_enabled) {
      fn.addFunctionUrl({
        authType: lambda.FunctionUrlAuthType.NONE, // 認証なし
      });
    }

    return fn;
  }

  /**
   * Create an API Gateway.
   * @param {lambda.Function} fn The Lambda function to be integrated.
   */
  makeApiGateway(fn: lambda.Function) {
    // REST API の定義
    const restapi = new apigateway.RestApi(this, "Notion-Api", {
      deployOptions: {
        stageName: "v1",
      },
      restApiName: "Notion-Api",
    });
    // ルートとインテグレーションの設定
    restapi.root.addMethod("ANY", new apigateway.LambdaIntegration(fn));
    restapi.root
      .addResource("{proxy+}")
      .addMethod("ANY", new apigateway.LambdaIntegration(fn));
    return restapi;
  }
}
