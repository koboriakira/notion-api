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

  @Step("Create a dummy gif/jpeg page")
  public async createImage() {
    const data = {
      images: [
        {
          file: "https://d3swar8tu7yuby.cloudfront.net/95babc77-87aa-43f9-8006-5d0c00f56260_dummy.png",
          thumbnail:
            "https://d3swar8tu7yuby.cloudfront.net/95babc77-87aa-43f9-8006-5d0c00f56260_dummy_thumb.png",
        },
      ],
    };
    const response = await client.post("/image/", data);
    const pageId = response.data.data[0].id;
    console.log(pageId);
    DataStoreFactory.getScenarioDataStore().put("pageId", pageId);
  }
}
