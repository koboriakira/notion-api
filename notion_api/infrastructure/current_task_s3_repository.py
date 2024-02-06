import json
import boto3
from typing import Optional
from datetime import datetime as DatetimeObject
from datetime import timedelta
from botocore.exceptions import NoCredentialsError
from domain.infrastructure.current_task_repository import CurrentTaskRepository
from custom_logger import get_logger
from util.datetime import JST

BUCKET_NAME = "notion-api-bucket-koboriakira"
FILE_NAME = "current_tasks.json"
FILE_PATH = "/tmp/" + FILE_NAME

logger = get_logger(__name__)

class CurrentTaskS3Repository(CurrentTaskRepository):
    def __init__(self):
        self.s3_client = boto3.client('s3')

    def save(self, tasks: list[dict]) -> bool:
        # current_tasks.jsonを出力
        five_minutes_later = DatetimeObject.now(JST) + timedelta(minutes=5)
        data = {
            "expires_at": five_minutes_later.isoformat(),
            "tasks": tasks
        }
        with open(FILE_PATH, 'w') as f:
            json.dump(tasks, f, indent=4)

        # S3にアップロード
        is_success = self.upload_to_s3()
        logger.info("is_success: " + str(is_success))
        return is_success

    def load(self) -> Optional[list[dict]]:
        # S3からダウンロード
        is_success = self.download_from_s3()
        if not is_success:
            logger.error("S3からのダウンロードに失敗しました。")
            return None

        # current_tasks.jsonを読み込み
        with open(FILE_PATH, 'r') as f:
            data = json.load(f)
            expires_at = DatetimeObject.fromisoformat(data["expires_at"])
            if expires_at.timestamp() < DatetimeObject.now(JST).timestamp():
                logger.warning("有効期限が切れています。")
                return None

            tasks: list[dict] = data["tasks"]
            return tasks


    def upload_to_s3(self) -> bool:
        try:
            # ファイルをアップロード
            self.s3_client.upload_file(FILE_PATH, BUCKET_NAME, FILE_NAME)
        except FileNotFoundError:
            logger.error("ファイルが見つかりませんでした。")
            return False
        except NoCredentialsError:
            logger.error("認証情報が不足しています。")
            return False
        except Exception as e:
            logger.error(e)
            return False
        return True

    def download_from_s3(self) -> bool:
        try:
            # ファイルをダウンロード
            self.s3_client.download_file(BUCKET_NAME, FILE_NAME, FILE_PATH)
        except FileNotFoundError:
            logger.error("ファイルが見つかりませんでした。")
            return False
        except NoCredentialsError:
            logger.error("認証情報が不足しています。")
            return False
        except Exception as e:
            logger.error(e)
            return False
        return True

if __name__ == '__main__':
    # python -m infrastructure.tasks_s3_repository
    print(TokenInfoS3Repository().save({"access_token": "test", "refresh_token": "test"}))
