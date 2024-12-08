/** @format */

import { Step, BeforeSuite, AfterSuite, DataStoreFactory } from "gauge-ts";
import { Axios } from "axios";
import Client from "./util/client";

let client: Axios;

export default class StepImplementation {
  @BeforeSuite()
  public async beforeSuite() {
    client = Client.generate();
  }

  @AfterSuite()
  public async afterSuite() {
    // do nothing
  }

  @Step("Create a food with name <title>")
  public async createFood(title: string) {
    const data = {
      title: title,
    };
    const response = await client.post("/food/", data);
    const pageId = response.data.data.id;
    DataStoreFactory.getScenarioDataStore().put("pageId", pageId);
  }
}
