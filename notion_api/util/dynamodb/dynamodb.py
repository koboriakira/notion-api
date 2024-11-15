import os
from typing import Any
import boto3

import custom_logger
from util.environment import Environment



dynamodb = None
if Environment.is_dev():
    dynamodb = boto3.resource(
        'dynamodb',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
        region_name=os.environ['AWS_DEFAULT_REGION']
    )
else:
    dynamodb = boto3.resource('dynamodb')

class DynamoDBClient:
    def __init__(self, table_name):
        self._table = dynamodb.Table(table_name) # type: ignore
        self._logger = custom_logger.get_logger(__name__)

    def put(self, item: dict) -> None:
        self._table.put_item(Item=item)

    def find(self, key_name: str, key_value: str) -> dict[str, Any]:
        response = self._table.get_item(Key={key_name: key_value})
        self._logger.debug("response: %s", response)

        if 'Item' in response:
            item = response['Item']
            print("アイテムを取得しました:", item)
            return item
        else:
            raise Exception("指定したキーのアイテムは存在しません")

if __name__ == '__main__':
    # python -m notion_api.util.dynamodb.dynamodb
    client = DynamoDBClient('NotionApi-NotionTableF26AF3BC-4263X0XU1OXU')
    # client.put({'key': '1', 'name': 'test'})
    # client.find('key', '1')
