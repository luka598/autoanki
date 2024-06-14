from dotenv import load_dotenv
from openai import OpenAI
import dataclasses as dc
import typing as T
import base64

load_dotenv()

client = OpenAI()


@dc.dataclass
class TextContent:
    text: str

    @property
    def as_dict(self):
        return {"type": "text", "text": self.text}


@dc.dataclass
class ImageUrlContent:
    url: str
    detail: T.Literal["low", "high", "auto"] = "auto"

    @property
    def as_dict(self):
        return {
            "type": "image_url",
            "image_url": {"url": self.url, "detail": self.detail},
        }

    @staticmethod
    def from_image(
        image: bytes, image_type: str, detail: T.Literal["low", "high", "auto"] = "auto"
    ):
        return ImageUrlContent(
            f"data:image/{image_type};base64,{base64.b64encode(image).decode('utf-8')}",
            detail,
        )

    @staticmethod
    def from_file(filename: str, detail: T.Literal["low", "high", "auto"] = "auto"):
        with open(filename, "rb") as f:
            return ImageUrlContent.from_image(f.read(), filename.split(".")[-1], detail)


@dc.dataclass
class Message:
    role: T.Literal["system", "user", "assistant"]
    content: T.Union[
        T.Union[TextContent, ImageUrlContent],
        T.List[T.Union[TextContent, ImageUrlContent]],
    ]

    @property
    def as_dict(self):
        if type(self.content) == list:  # noqa: E721
            return {
                "role": self.role,
                "content": [item.as_dict for item in self.content],
            }
        elif type(self.content) == TextContent:
            return {
                "role": self.role,
                "content": self.content.text,
            }
        elif type(self.content) == ImageUrlContent:
            return {
                "role": self.role,
                "content": [self.content.as_dict],
            }
        else:
            raise RuntimeError(
                "What??",
                self.content,
                type(self.content),
            )


@dc.dataclass
class Request:
    model: T.Literal["gpt-4o", "gpt-3.5-turbo"]
    messages: T.List[Message]
    max_tokens: int = 300
    stream = False

    @property
    def as_dict(self):
        return {
            "model": self.model,
            "messages": [item.as_dict for item in self.messages],
            "max_tokens": self.max_tokens,
            "stream": self.stream,
        }


class Response:
    content: str
    tokens: T.Tuple[int, int]
    end_code: str
    original: T.Any

    def __init__(self, response: T.Any) -> None:
        self.content = response.choices[0].message.content
        self.tokens = (response.usage.prompt_tokens, response.usage.completion_tokens)
        self.end_code = response.choices[0].finish_reason
        self.original = response

    def __repr__(self) -> str:
        r = "--- BEGIN RESPONSE ---\n"
        r += f"Input tokens: {self.tokens[0]} (${self.cost[0]:.4f})\n"
        r += f"Output tokens: {self.tokens[1]} (${self.cost[1]:.4f})\n"
        r += f"Total tokens: {self.tokens[0] + self.tokens[1]} (${self.cost[0]+self.cost[1]:.4f})\n"
        r += f"End code: {self.end_code}\n"
        r += "-- CONTENT --\n"
        r += self.content + "\n"
        r += "-- ORIGINAL --\n"
        r += repr(self.original) + "\n"
        r += "--- END RESPONSE ---\n"
        return r

    @property
    def cost(self):
        return (self.tokens[0] * (5 / 1_000_000), self.tokens[1] * (15 / 1_000_000))


def send(request: Request) -> Response:
    return Response(client.chat.completions.create(**request.as_dict))
