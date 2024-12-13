import json

from lotion import Lotion


def get_select(
    database_id: str,
    name: str,
) -> None:
    # python -m notion_api.task.domain.task_context
    pages = Lotion.get_instance().retrieve_database(database_id=database_id)

    result = {}
    for page in pages:
        select_property = page.get_select(name=name)
        if select_property is None:
            continue
        if select_property.selected_id in result:
            continue
        result[select_property.selected_name] = {
            "selected_id": select_property.selected_id,
            "selected_color": select_property.selected_color,
        }
    print(json.dumps(result, ensure_ascii=False))
