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
  aws_sqs as sqs,
  aws_dynamodb as dynamodb,
} from "aws-cdk-lib";
import { Construct } from "constructs";
import { SCHEDULER_CONFIG } from "./event_bridge_scheduler";
import { convertToCamelCase } from "./utils";
import { Timeout } from "aws-cdk-lib/aws-stepfunctions";

// CONFIG
const RUNTIME = lambda.Runtime.PYTHON_3_12;
const TIMEOUT = 30;
const BATCH_TIMEOUT = 300;
const APP_DIR_PATH = "../notion_api";
const LAYER_ZIP_PATH = "../dependencies.zip";

export class NotionApi extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    // dynamoDBの作成
    const notionDynamoDb = new dynamodb.Table(this, "NotionTable", {
      tableName: "NotionApiAttributes",
      partitionKey: {
        name: "key",
        type: dynamodb.AttributeType.STRING,
      },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
      removalPolicy: RemovalPolicy.DESTROY,
    });

    const role = this.makeRole(notionDynamoDb.tableArn);
    const myLayer = this.makeLayer();

    // FastAPI(API Gateway)の作成
    const main = this.createLambdaFunction("main", role, myLayer);
    this.makeApiGateway(main);

    // イベントルールとLambdaの作成
    Object.entries(SCHEDULER_CONFIG).forEach(([key, schedule]) => {
      this.createEventLambda(key, role, myLayer, schedule);
    });

    // SQSから呼び出されるイベントの作成
    this.createLambdaAndSqs("create_page", role, myLayer, main);
  }

  createLambdaAndSqs(
    handlerName: string,
    role: iam.Role,
    myLayer: lambda.LayerVersion,
    send_message_function: lambda.Function,
    timeout: number = 300
  ) {
    const fn = this.createLambdaFunction(
      handlerName,
      role,
      myLayer,
      false,
      timeout,
      true
    );
    const appName = convertToCamelCase(handlerName);
    const queue = new sqs.Queue(this, `${appName}Queue`, {
      visibilityTimeout: Duration.seconds(300),
    });
    queue.grantConsumeMessages(fn);
    queue.grantSendMessages(send_message_function);
    fn.addEventSourceMapping(`${appName}EventSource`, {
      eventSourceArn: queue.queueArn,
      batchSize: 1,
    });
    return fn;
  }

  createEventLambda(
    handlerName: string,
    role: iam.Role,
    myLayer: lambda.LayerVersion,
    schedule: events.Schedule
  ): lambda.Function {
    const fn = this.createLambdaFunction(
      handlerName,
      role,
      myLayer,
      false,
      BATCH_TIMEOUT
    );
    new events.Rule(this, `${convertToCamelCase(handlerName)}Rule`, {
      schedule: schedule,
      targets: [new targets.LambdaFunction(fn, { retryAttempts: 0 })],
    });
    return fn;
  }

  /**
   * Create or retrieve an IAM role for the Lambda function.
   * @returns {iam.Role} The created or retrieved IAM role.
   */
  makeRole(dynamoDbArn: string): iam.Role {
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

    // dynamoDBにアクセスするための権限
    role.addToPrincipalPolicy(
      new iam.PolicyStatement({
        actions: ["dynamodb:*"],
        resources: [dynamoDbArn],
      })
    );

    // SQSにメッセージを送信するために必要な権限
    role.addToPrincipalPolicy(
      new iam.PolicyStatement({
        actions: ["sqs:sendMessage"],
        resources: ["*"],
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
    handlerName: string,
    role: iam.Role,
    myLayer: lambda.LayerVersion,
    function_url_enabled: boolean = false,
    timeout: number = TIMEOUT,
    deadLetterQueueEnabled: boolean = false
  ): lambda.Function {
    const resourceNameCamel = convertToCamelCase(handlerName);

    const fn = new lambda.Function(this, resourceNameCamel, {
      runtime: RUNTIME,
      handler: handlerName + ".handler",
      code: lambda.Code.fromAsset(APP_DIR_PATH),
      role: role,
      layers: [myLayer],
      timeout: Duration.seconds(timeout),
      deadLetterQueueEnabled: deadLetterQueueEnabled,
    });

    fn.addEnvironment("NOTION_SECRET", process.env.NOTION_SECRET || "");
    fn.addEnvironment(
      "UNSPLASH_ACCESS_KEY",
      process.env.UNSPLASH_ACCESS_KEY || ""
    );
    fn.addEnvironment("SLACK_BOT_TOKEN", process.env.SLACK_BOT_TOKEN || "");
    fn.addEnvironment("SLACK_USER_TOKEN", process.env.SLACK_USER_TOKEN || "");
    fn.addEnvironment("AWS_ACCOUNT_ID", process.env.AWS_ACCOUNT_ID || "");
    fn.addEnvironment("OPENAI_API_KEY", process.env.OPENAI_API_KEY || "");
    fn.addEnvironment(
      "LAMBDA_SLACK_CONCIERGE_API_DOMAIN",
      process.env.LAMBDA_SLACK_CONCIERGE_API_DOMAIN || ""
    );
    fn.addEnvironment(
      "LAMBDA_TWITTER_API_DOMAIN",
      process.env.LAMBDA_TWITTER_API_DOMAIN || ""
    );
    fn.addEnvironment(
      "LAMBDA_GOOGLE_CALENDAR_API_DOMAIN",
      process.env.LAMBDA_GOOGLE_CALENDAR_API_DOMAIN || ""
    );
    fn.addEnvironment(
      "LAMBDA_GOOGLE_CALENDAR_API_ACCESS_TOKEN",
      process.env.LAMBDA_GOOGLE_CALENDAR_API_ACCESS_TOKEN || ""
    );

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
