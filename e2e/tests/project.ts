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

  @Step("Create a project with specified request")
  public async createProjectWithSpecifiedRequest() {
    const data = {
      data: {
        object: "page",
        id: "1566567a-3bbf-80a6-8e92-ff97eb64b8c9",
        properties: {
          名前: {
            id: "title",
            type: "title",
            title: [
              {
                type: "text",
                text: {
                  content: "テストプロジェクト",
                  link: null,
                },
                annotations: {
                  bold: false,
                  italic: false,
                  strikethrough: false,
                  underline: false,
                  code: false,
                  color: "default",
                },
                plain_text: "テストプロジェクト",
                href: null,
              },
            ],
          },
          プロジェクト名: {
            id: "N%3Eat",
            type: "rich_text",
            rich_text: [
              {
                type: "text",
                text: {
                  content: "テストプロジェクト1",
                  link: null,
                },
                annotations: {
                  bold: false,
                  italic: false,
                  strikethrough: false,
                  underline: false,
                  code: false,
                  color: "default",
                },
                plain_text: "テストプロジェクト1",
                href: null,
              },
            ],
          },
        },
      },
    };
    const response = await client.post("/projects/", data);
    // const pageId = response.data.data.id;
    // DataStoreFactory.getScenarioDataStore().put("pageId", pageId);
  }
}
