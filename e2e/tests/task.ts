
import { Step, Table, BeforeSuite, AfterSuite, DataStoreFactory } from "gauge-ts";
import * as https from 'https';
import { strictEqual } from 'assert';
import { checkBox, click, closeBrowser, evaluate, goto, into, link, openBrowser, press, text, textBox, toLeftOf, write } from 'taiko';
import assert = require("assert");
import axios, { Axios } from "axios";

let client: Axios

export default class StepImplementation {
  @BeforeSuite()
  public async beforeSuite() {
    client = axios.create({
      baseURL: "http://localhost:10119",
      headers: {
        "access-token": "secret_ppD3MX1zozBvsAL2I1lUBSpnufCz22u174t9e5PukuW",
      },
      httpsAgent: new https.Agent({ rejectUnauthorized: false })
    });
  }

  @AfterSuite()
  public async afterSuite() {
    // do nothing
  };

  @Step("Create a task with name <title>")
  public async createTask(title: string) {
    // http://localhost:10119/tasks にPOSTリクエストを送信する
    // タスクのタイトルは <title> で指定される
    const data = {
      title: title
    }
    const response = await client.post("/task/", data)
    const pageId = response.data.data.id
    DataStoreFactory.getScenarioDataStore().put("pageId", pageId)
  }
}
