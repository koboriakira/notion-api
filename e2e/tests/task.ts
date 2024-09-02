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

  @Step("Create a task with name <title>")
  public async createTask(title: string) {
    const data = {
      title: title
    }
    const response = await client.post("/task/", data)
    const pageId = response.data.data.id
    DataStoreFactory.getScenarioDataStore().put("pageId", pageId)
  }

  @Step("Complete a task with name <title>")
  public async completeTask(title: string) {
    const data = {
      status: "Done"
    }
    const taskId = DataStoreFactory.getScenarioDataStore().get("pageId")
    const _response = await client.post(`/task/${taskId}/complete/`, data)
  }

  @Step("Create a task with name <title> and kind <kind>")
  public async createTaskWithKind(title: string, kind: string) {
    const data = {
      title: title,
      kind: kind,
      "start_date": new Date().toISOString(),
    }
    const response = await client.post("/task/", data)
    const pageId = response.data.data.id
    DataStoreFactory.getScenarioDataStore().put("pageId", pageId)
  }
}
