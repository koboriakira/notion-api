#!/usr/bin/env node
/** @format */

import "source-map-support/register";
import * as cdk from "aws-cdk-lib";
import { NotionApi } from "../lib/notion-api";

const app = new cdk.App();
new NotionApi(app, "NotionApi", {});
