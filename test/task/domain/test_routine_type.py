from datetime import date

import pytest
from notion_api.task.domain.routine_task import RoutineType

# 2024年3月20日(水)
BASIS_DATE_WED = date(2024, 3, 20)
BASIS_DATE_SUN = date(2024, 3, 24)


@pytest.mark.parametrize(
    ["basis_date", "suite", "expected"],
    [
        pytest.param(BASIS_DATE_WED, RoutineType.DAILY, date(2024, 3, 20), id="DAILY"),
        pytest.param(BASIS_DATE_WED, RoutineType.EVERY_SAT, date(2024, 3, 23), id="EVERY_SAT"),
        pytest.param(BASIS_DATE_WED, RoutineType.EVERY_TUE_AND_FRI, date(2024, 3, 22), id="EVERY_TUE_AND_FRI"),
        pytest.param(BASIS_DATE_WED, RoutineType.EVERY_WED, date(2024, 3, 20), id="EVERY_WED"),
        pytest.param(BASIS_DATE_WED, RoutineType.DAYS_AFTER_7, date(2024, 3, 27), id="DAYS_AFTER_7"),
        pytest.param(BASIS_DATE_WED, RoutineType.DAYS_AFTER_3, date(2024, 3, 23), id="DAYS_AFTER_3"),
        pytest.param(BASIS_DATE_SUN, RoutineType.DAILY, date(2024, 3, 24), id="DAILY_2"),
        pytest.param(BASIS_DATE_SUN, RoutineType.EVERY_SAT, date(2024, 3, 30), id="EVERY_SAT_2"),
        pytest.param(BASIS_DATE_SUN, RoutineType.EVERY_TUE_AND_FRI, date(2024, 3, 26), id="EVERY_TUE_AND_FRI_2"),
        pytest.param(BASIS_DATE_SUN, RoutineType.EVERY_WED, date(2024, 3, 27), id="EVERY_WED_2"),
    ],
)
def test_次のルーティン実行日を取得する(basis_date: date, suite: RoutineType, expected: date):
    assert suite.next_date(basis_date) == expected
