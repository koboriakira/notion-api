import json
from collections.abc import Callable
from logging import Logger, getLogger

from openai import OpenAI
from openai.types.chat.chat_completion_message import ChatCompletionMessageToolCall

OPENAI_MODEL_DEFAULT = "gpt-4o-mini"


class FunctionCallingError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

    @staticmethod
    def tool_not_found(func: Callable) -> "FunctionCallingError":
        return FunctionCallingError(f"tool not found: {func.__name__}")


class OpenaiExecuter:
    def __init__(self, model: str = OPENAI_MODEL_DEFAULT, logger: Logger | None = None) -> None:
        self.model = model
        self.logger = logger or getLogger(__name__)
        self.client = OpenAI()

    def simple_chat(self, user_content: str) -> str:
        """メッセージをOpenAIに送信して、返答を受け取る"""
        assert isinstance(user_content, str)

        messages = [{"role": "user", "content": user_content}]
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=1,
        )
        self.logger.debug(response.choices[0].message)
        content = response.choices[0].message.content
        if response.usage:
            completion_tokens = response.usage.completion_tokens
            prompt_tokens = response.usage.prompt_tokens
            print(f"prompt_tokens: {prompt_tokens}, completion_tokens: {completion_tokens}")
        return content or ""

    def simple_json_chat(self, system_prompt: str, user_content: str) -> dict:
        """メッセージをOpenAIに送信して、返答を受け取る"""
        assert isinstance(system_prompt, str)
        assert isinstance(user_content, str)
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ]
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            response_format={"type": "json_object"},
        )
        message = response.choices[0].message
        try:
            return json.loads(message.content)
        except json.JSONDecodeError as e:
            print(message.content)
            return e

    def simple_function_calling(
        self,
        user_content: str,
        func: Callable,
        func_description: str,
        parameters: dict,
    ) -> any:
        """
        シンプルな単一のfunction callingを実行して、実行結果を受け取る

        注意:
            funcの引数は、"args"という名前でdict型である必要がある。
            そのdictの中にOpenAIが出力した「関数に使う引数」がすべて入っている。
            それ以外の引数は受け取れない。
        """
        assert isinstance(user_content, str)
        assert callable(func)
        assert isinstance(func_description, str)
        assert isinstance(parameters, dict)

        tool_calls = self.__function_calling(
            user_content=user_content,
            func=func,
            func_description=func_description,
            parameters=parameters,
        )
        if not tool_calls or len(tool_calls) == 0:
            raise FunctionCallingError.tool_not_found(func)

        tool_call = tool_calls[0]
        args = tool_call.function.arguments
        return func(args=args)

    def __function_calling(
        self,
        user_content: str,
        func: Callable,
        func_description: str,
        parameters: dict,
    ) -> list[ChatCompletionMessageToolCall]:
        messages = [{"role": "user", "content": user_content}]
        tool = {
            "type": "function",
            "function": {
                "name": func.__name__,
                "description": func_description,
                "parameters": parameters,
            },
        }
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=[tool],
            tool_choice="auto",
        )
        response_message = response.choices[0].message
        return response_message.tool_calls


if __name__ == "__main__":
    # python -m notion_api.util.openai_executer
    suite = OpenaiExecuter()
    print(suite.simple_chat("hello"))
