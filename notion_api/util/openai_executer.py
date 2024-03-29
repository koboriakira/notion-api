import json
from collections.abc import Callable
from logging import Logger, getLogger

from openai import OpenAI

OPENAI_MODEL_DEFAULT = "gpt-3.5-turbo-1106"


class OpenaiExecuter:
    def __init__(
            self,
            model: str = OPENAI_MODEL_DEFAULT,
            logger: Logger | None = None) -> None:
        self.model = model
        self.logger = logger or getLogger(__name__)
        self.client = OpenAI()

    def simple_chat(self, user_content: str) -> str:
        """メッセージをOpenAIに送信して、返答を受け取る"""
        messages = [{"role": "user", "content": user_content}]
        response_message = self.__chat_completions_create(messages=messages)
        self.logger.debug(response_message)
        return response_message.content

    def simple_function_calling(
            self,
            user_content: str,
            func: Callable,
            func_description: str,
            parameters: dict):
        """
        シンプルな単一のfunction callingを実行して、実行結果を受け取る

        注意:
            funcの引数は、"args"という名前でdict型である必要がある。
            そのdictの中にOpenAIが出力した「関数に使う引数」がすべて入っている。
            それ以外の引数は受け取れない。
        """
        messages = [{"role": "user", "content": user_content}]
        tools = [
            {
                "type": "function",
                "function": {
                    "name": func.__name__,
                    "description": func_description,
                    "parameters": parameters,
                },
            },
        ]
        response_message = self.__chat_completions_create(
            messages=messages, tools=tools, tool_choice="auto",
        )
        tool_calls = response_message.tool_calls
        if not tool_calls or len(tool_calls) == 0:
            self.logger.warning("tool_calls is empty")
            return None

        available_functions = {
            func.__name__: func,
        }
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            return function_to_call(args=function_args)
        exception_msg = "tool_call is not found"
        raise Exception(exception_msg)

    def __chat_completions_create(
            self,
            messages: list[dict],
            tools: list[dict] | None = None,
            tool_choice: str | None = None):
        """OpenAIのchat_completions.createを呼び出す"""
        if tools is None or tool_choice is None:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
            )
            self.logger.debug(response)
            return response.choices[0].message
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )
        self.logger.debug(response)
        return response.choices[0].message
