import sys
from dataclasses import dataclass


@dataclass
class TaskOrder:
    value: int

    @classmethod
    def not_important(cls, subtracted_num: int = 0) -> "TaskOrder":
        """優先度最低"""
        return TaskOrder(sys.maxsize - subtracted_num)

    @classmethod
    def normal(cls, added_num: int = 0) -> "TaskOrder":
        """優先度普通"""
        return TaskOrder(int(sys.maxsize / 2) - added_num)

    @classmethod
    def most_important(cls) -> "TaskOrder":
        """優先度最高"""
        return TaskOrder(0)

    @classmethod
    def important(cls, added_num: int = 0) -> "TaskOrder":
        """優先度高"""
        return TaskOrder(1 + added_num)
