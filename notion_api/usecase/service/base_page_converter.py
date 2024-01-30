from notion_client_wrapper.base_page import BasePage

class BasePageConverter:
    @staticmethod
    def to_task(page: BasePage) -> dict:
        status = page.get_status(name="ステータス")
        start_date = page.get_date(name="実施日")
        task_kind = page.get_select(name="タスク種別")
        feeling = page.get_text(name="気持ち")
        return {
            "id": page.id,
            "url": page.url,
            "title": page.get_title().text,
            "created_at": page.created_time.value,
            "updated_at": page.last_edited_time.value,
            "status": status.status_name,
            "task_kind": task_kind.name if task_kind is not None else None,
            "start_date": start_date.start if start_date is not None else None,
            "end_date": start_date.end if start_date is not None else None,
            "feeling": feeling.text,
        }
