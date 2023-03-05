import openai
from defines import ErrorCode
from settings import OPEN_KEY

openai.api_key = OPEN_KEY


class ChatGPTService:
    def models(cls):
        return openai.Model.list()

    @classmethod
    def fetch(cls, content, model=None, role=None):
        role = role or "user"
        model = model or "gpt-3.5-turbo"
        messages = [
            {"role": "user", "content": content}
        ]

        try:
            completion = openai.ChatCompletion.create(
                model=model,
                messages=messages
            )

            ret = completion.choices[0].message  # {"content": "", "role": ""}
        except Exception as ex:
            return ErrorCode.ERROR, f"{ex}"

        return ErrorCode.SUCC, ret
