from datetime import date, datetime, timedelta

from notion_databases.task_prop.task_kind import TaskKindType
from task.task_order import TaskOrder
from util.datetime import jst_now


class TaskOrderRule:
    @classmethod
    def calculate(
        cls,
        start_datetime: datetime | date | None,
        kind: TaskKindType | None,
    ) -> TaskOrder:
        """
        重要度の計算。おおまかな指針としては次の通り
        - 開始時刻もしくは締め切り時刻が現時刻から30分以内、もしくは現時刻を過ぎている場合は重要とする
        - 上記にあてはまらないルーティンは重要度最低とする
        - そのほかは原則タスク種別ごとに並べる
        """
        # 調整用の数値。重要とみなせば値を小さくし、重要でなければ大きくする
        num = 1

        # 開始時刻もしくは締め切り時刻が現時刻を過ぎている場合は重要とする
        if _is_run_over(start_datetime):
            return TaskOrder.important(num)
        num += 1

        # 開始時刻もしくは締め切り時刻が現時刻から30分以内の場合は重要とする
        if _within_minutes(start_datetime, 30):
            return TaskOrder.important(num)

        # ルーティンは重要度最低とする
        if kind == TaskKindType.ROUTINE:
            return TaskOrder.not_important()

        # そのほかは原則タスク種別ごとに並べる
        if kind is not None:
            # kindの優先度が高いほどorderを小さくする
            return TaskOrder.normal(added_num=kind.priority)
        return TaskOrder.normal()


def _is_run_over(datetime_: datetime | date | None) -> bool:
    """現時刻を過ぎているかどうかを判定"""
    if datetime_ is None:
        return False
    if not isinstance(datetime_, datetime) or datetime_.time() == datetime.min.time():
        return False
    return datetime_.timestamp() <= jst_now().timestamp()


def _within_minutes(datetime_: datetime | date | None, minutes: int) -> bool:
    """指定した分数以内かどうかを判定"""
    if datetime_ is None:
        return False
    if not isinstance(datetime_, datetime) or datetime_.time() == datetime.min.time():
        return False
    after_datetime = (datetime_ + timedelta(minutes=minutes)).timestamp()
    now = jst_now().timestamp()
    return datetime_.timestamp() <= now and now <= after_datetime
