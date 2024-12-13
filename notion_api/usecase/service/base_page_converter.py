from lotion.base_page import BasePage


class BasePageConverter:
    @staticmethod
    def to_task(page: BasePage) -> dict:
        status = page.get_status(name="ステータス")
        start_date = page.get_date(name="実施日")
        task_kind = page.get_select(name="タスク種別")
        slack_text_list = [block.to_slack_text() for block in page.block_children]
        text = "\n".join(slack_text_list)
        return {
            "id": page.id,
            "url": page.url,
            "title": page.get_title_text(),
            "created_at": page.get_created_at().isoformat(),
            "updated_at": page.get_updated_at().isoformat(),
            "status": status.status_name,
            "task_kind": task_kind.name if task_kind is not None else None,
            "start_date": start_date.start if start_date is not None else None,
            "end_date": start_date.end if start_date is not None else None,
            "text": text,
        }
