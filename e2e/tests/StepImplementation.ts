/** @format */

import {
  Step,
  Table,
  BeforeSuite,
  AfterSuite,
  DataStoreFactory,
} from "gauge-ts";
import * as https from "https";
import { strictEqual } from "assert";
import {
  checkBox,
  click,
  closeBrowser,
  evaluate,
  goto,
  into,
  link,
  openBrowser,
  press,
  text,
  textBox,
  toLeftOf,
  write,
} from "taiko";
import assert = require("assert");
import axios, { Axios } from "axios";

let client: Axios;

export default class StepImplementation {
  @BeforeSuite()
  public async beforeSuite() {
    client = axios.create({
      baseURL: "http://localhost:10119",
      headers: {
        "access-token": "secret_ppD3MX1zozBvsAL2I1lUBSpnufCz22u174t9e5PukuW",
      },
      httpsAgent: new https.Agent({ rejectUnauthorized: false }),
    });
  }

  @AfterSuite()
  public async afterSuite() {
    // await closeBrowser();
  }

  @Step("Delete the latest created page")
  public async deleteLatestPage() {
    const pageId = DataStoreFactory.getScenarioDataStore().get("pageId");
    const response = await client.delete(`/page/${pageId}`);
  }

  @Step("Delete the latest created project")
  public async deleteLatestProject() {
    const pageId = DataStoreFactory.getScenarioDataStore().get("projectId");
    const response = await client.delete(`/projects/${pageId}/`);
  }

  @Step("Append a sample image in page <pageId>")
  public async appendSampleImage(pageId: string) {
    const data = {
      image_url: "https://d3swar8tu7yuby.cloudfront.net/IMG_6286_thumb.jpg",
    };
    const response = await client.post(`/page/${pageId}/image/`, data);
  }

  @Step("Open todo application")
  public async openTodo() {
    await goto("todo.taiko.dev");
  }

  @Step("Add task <item>")
  public async addTask(item: string) {
    await write(
      item,
      into(
        textBox({
          class: "new-todo",
        })
      )
    );
    await press("Enter");
  }

  @Step("Must display <message>")
  public async checkDisplay(message: string) {
    assert.ok(await text(message).exists(0, 0));
  }

  @Step("Add tasks <table>")
  public async addTasks(table: Table) {
    for (var row of table.getTableRows()) {
      await write(row.getCell("description"));
      await press("Enter");
    }
  }

  @Step("Complete tasks <table>")
  public async completeTasks(table: Table) {
    for (var row of table.getTableRows()) {
      await click(checkBox(toLeftOf(row.getCell("description"))));
    }
  }

  @Step("View <type> tasks")
  public async viewTasks(type: string) {
    await click(link(type));
  }

  @Step("Must have <table>")
  public async mustHave(table: Table) {
    for (var row of table.getTableRows()) {
      assert.ok(await text(row.getCell("description")).exists());
    }
  }

  @Step("Must not have <table>")
  public async mustNotHave(table: Table) {
    for (var row of table.getTableRows()) {
      assert.ok(!(await text(row.getCell("description")).exists(0, 0)));
    }
  }

  @Step("Clear all tasks")
  public async clearAllTasks() {
    // @ts-ignore
    await evaluate(() => localStorage.clear());
  }
}
