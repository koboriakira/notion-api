import os
from notion_client_wrapper.client_wrapper import ClientWrapper
from model.database_type import DatabaseType

class ProjectListUseCase:
    def __init__(self):
        self.client = ClientWrapper(notion_secret=os.getenv("NOTION_SECRET"))

    def execute(self):
        projects = self.client.retrieve_database(database_id=DatabaseType.PROJECT.value)
        print(projects)
        return []
