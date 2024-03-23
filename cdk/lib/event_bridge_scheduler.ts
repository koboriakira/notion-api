/** @format */

import { aws_events as events } from "aws-cdk-lib";

/**
 * キー名: ハンドラー名（ファイル名）
 * 値: スケジュール設定
 */
export const SCHEDULER_CONFIG = {
  // 月曜10時に実行
  create_daily_log: events.Schedule.cron({
    minute: "0",
    hour: "1",
    month: "*",
    year: "*",
    weekDay: "MON",
  }),
  // 10分ごとに実行
  clean_empty_title_page: events.Schedule.cron({
    minute: "*/10",
    hour: "*",
    month: "*",
    year: "*",
    weekDay: "*",
  }),
  // 毎日21時に実行
  collect_updated_pages: events.Schedule.cron({
    minute: "0",
    hour: "12",
    month: "*",
    year: "*",
    weekDay: "*",
  }),
  // 毎日2時に実行
  postpone_task: events.Schedule.cron({
    minute: "0",
    hour: "17",
    month: "*",
    year: "*",
    weekDay: "*",
  }),
  // 3分ごとに実行(8時から24時まで)
  // update_current_tasks: events.Schedule.cron({
  //   minute: "*/3",
  //   hour: "23-15",
  //   month: "*",
  //   year: "*",
  //   weekDay: "*",
  // }),
  // 毎日2時5分に実行
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
};
