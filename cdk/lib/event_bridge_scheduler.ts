/** @format */

import { aws_events as events } from "aws-cdk-lib";

/**
 * キー名: ハンドラー名（ファイル名）
 * 値: スケジュール設定
 */
export const SCHEDULER_CONFIG = {
  // 5分ごとに実行。できればもっと短い間隔で実行したいけど、コストを考えて
  every_minutes_batch: events.Schedule.cron({
    minute: "*/5",
    hour: "*",
    month: "*",
    year: "*",
    weekDay: "*",
  }),
  // 月曜10時に実行
  create_daily_log: events.Schedule.cron({
    minute: "0",
    hour: "1",
    month: "*",
    year: "*",
    weekDay: "MON",
  }),
  // 毎日3時に実行
  postpone_task: events.Schedule.cron({
    minute: "0",
    hour: "18",
    month: "*",
    year: "*",
    weekDay: "*",
  }),
  move_completed_task_to_backup: events.Schedule.cron({
    minute: "5",
    hour: "17",
    month: "*",
    year: "*",
    weekDay: "*",
  }),
  // 毎日5時に実行
  create_routine_task: events.Schedule.cron({
    minute: "0",
    hour: "20",
    month: "*",
    year: "*",
    weekDay: "*",
  }),
  // 毎日12時に実行
  remind_zettlekasten: events.Schedule.cron({
    minute: "0",
    hour: "3",
    month: "*",
    year: "*",
    weekDay: "*",
  }),
};
