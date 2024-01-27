from enum import Enum

class StatusEnum(Enum):
    """
    Notionで利用するすべてのステータス一覧
    逆にNotionのステータス選択肢は、このEnumに含まれるもののみとする
    """
    TODO= "ToDo"
    IN_PROGRESS = "InProgress"
    DONE = "Done"

    @staticmethod
    def get_status(value:str) -> 'StatusEnum':
        for status in StatusEnum:
            if status.value.upper() == value.upper():
                return status
        raise ValueError(f"Invalid status value: {value}")


    @staticmethod
    def get_status_list(status_list: list[str]) -> list['StatusEnum']:
        if len(status_list) == 0:
            return [s for s in StatusEnum]

        result: list[StatusEnum] = []
        for status_str in status_list:
            for status in StatusEnum:
                if status.value.upper() == status_str.upper():
                    result.append(status)
                    break
        return result
