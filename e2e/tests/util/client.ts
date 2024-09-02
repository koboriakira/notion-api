import * as https from 'https';
import axios, { Axios } from "axios";

require('dotenv').config();

export default class Client {
  public static generate(): Axios {
    return axios.create({
      baseURL: "http://localhost:10119",
      headers: {
        "access-token": process.env.NOTION_SECRET,
      },
      httpsAgent: new https.Agent({ rejectUnauthorized: false })
    });
  }
}
