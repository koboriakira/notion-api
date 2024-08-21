import { Step, BeforeSuite, AfterSuite, DataStoreFactory } from "gauge-ts";
import * as https from 'https';
import assert = require("assert");
import axios, { Axios } from "axios";

require('dotenv').config();
let client: Axios
export default class StepImplementation {
  @BeforeSuite()
  public async beforeSuite() {
    client = axios.create({
      baseURL: "http://localhost:10119",
      headers: {
        "access-token": process.env.NOTION_SECRET,
      },
      httpsAgent: new https.Agent({ rejectUnauthorized: false })
    });
  }

  @AfterSuite()
  public async afterSuite() {
    // do nothing
  };

  @Step("Create a account book with title <title> and price <price>")
  public async createTaskWithKind(title: string, price: number) {
    // http://localhost:10119/tasks にPOSTリクエストを送信する
    // タスクのタイトルは <title> で指定される
    const data = {
      title: title,
      price: price,
    }
    const response = await client.post("/account_book/", data)
    const pageId = response.data.data.id
    DataStoreFactory.getScenarioDataStore().put("pageId", pageId)
  }
}
