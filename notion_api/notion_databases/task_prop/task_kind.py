from enum import Enum


class TaskKindType(Enum):
    TRASH = "ゴミ箱"
    WAIT = "待ち"
    DO_NOW = "今すぐやる"
    NEXT_ACTION = "次にとるべき行動リスト"
    SOMEDAY_MAYBE = "いつかやる・たぶんやる"
    SCHEDULE = "スケジュール"
    ROUTINE = "ルーティン"
    HABIT = "習慣"
    THIS_WEEK = "今週の目標"
    INTERRUPTION = "差し込み"
    NONE = ""

    @property
    def priority(self) -> int:
        return {
            TaskKindType.TRASH: 0,
            TaskKindType.ROUTINE: 1,
            TaskKindType.WAIT: 2,
            TaskKindType.SOMEDAY_MAYBE: 3,
            TaskKindType.SCHEDULE: 4,
            TaskKindType.NEXT_ACTION: 5,
            TaskKindType.DO_NOW: 6,
            TaskKindType.HABIT: 7,
            TaskKindType.NONE: 8,
            TaskKindType.THIS_WEEK: 9,
            TaskKindType.INTERRUPTION: 10,
        }[self]
