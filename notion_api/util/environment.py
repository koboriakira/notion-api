import os


class Environment:
    @staticmethod
    def is_dev() -> bool:
        return os.environ.get("ENVIRONMENT") == "dev"

    @staticmethod
    def get_dm_channel() -> str:
        return "D0572EG3TN3"
