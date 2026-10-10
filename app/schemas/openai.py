from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class OpenAIModelInfo(BaseModel):
    id: str
    object: str = "model"
    created: int
    owned_by: str = "moviepilot"


class OpenAIModelListResponse(BaseModel):
    object: str = "list"
    data: list[OpenAIModelInfo] = Field(default_factory=list)


class OpenAIChatMessage(BaseModel):
    role: str
    content: Any
    name: str | None = None

    model_config = ConfigDict(extra="allow")


class OpenAIChatCompletionsRequest(BaseModel):
    model: str | None = None
    messages: list[OpenAIChatMessage]
    user: str | None = None
    stream: bool = False

    model_config = ConfigDict(extra="allow")


class OpenAIResponsesRequest(BaseModel):
    model: str | None = None
    input: Any
    instructions: str | None = None
    user: str | None = None
    stream: bool = False

    model_config = ConfigDict(extra="allow")


class OpenAIChatChoiceMessage(BaseModel):
    role: str = "assistant"
    content: str


class OpenAIChatChoice(BaseModel):
    index: int = 0
    message: OpenAIChatChoiceMessage
    finish_reason: str = "stop"


class OpenAIUsage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class OpenAIChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: list[OpenAIChatChoice]
    usage: OpenAIUsage


class OpenAIResponsesOutputText(BaseModel):
    type: str = "output_text"
    text: str
    annotations: list[dict[str, Any]] = Field(default_factory=list)


class OpenAIResponsesOutputMessage(BaseModel):
    id: str
    type: str = "message"
    status: str = "completed"
    role: str = "assistant"
    content: list[OpenAIResponsesOutputText] = Field(default_factory=list)


class OpenAIResponsesResponse(BaseModel):
    id: str
    object: str = "response"
    created_at: int
    status: str = "completed"
    model: str
    output: list[OpenAIResponsesOutputMessage] = Field(default_factory=list)
    error: Any | None = None
    incomplete_details: Any | None = None
    usage: OpenAIUsage


class OpenAIErrorDetail(BaseModel):
    message: str
    type: str = "invalid_request_error"
    param: str | None = None
    code: str | None = None


class OpenAIErrorResponse(BaseModel):
    error: OpenAIErrorDetail


OpenAIChatContentPart = dict[str, Any]


class AnthropicMessage(BaseModel):
    role: str
    content: Any

    model_config = ConfigDict(extra="allow")


class AnthropicMessagesRequest(BaseModel):
    model: str | None = None
    messages: list[AnthropicMessage]
    system: Any | None = None
    max_tokens: int | None = 1024
    stream: bool = False

    model_config = ConfigDict(extra="allow")


class AnthropicTextBlock(BaseModel):
    type: str = "text"
    text: str


class AnthropicUsage(BaseModel):
    input_tokens: int = 0
    output_tokens: int = 0


class AnthropicMessagesResponse(BaseModel):
    id: str
    type: str = "message"
    role: str = "assistant"
    content: list[AnthropicTextBlock] = Field(default_factory=list)
    model: str
    stop_reason: str = "end_turn"
    stop_sequence: str | None = None
    usage: AnthropicUsage = Field(default_factory=AnthropicUsage)


class AnthropicErrorDetail(BaseModel):
    type: str = "invalid_request_error"
    message: str


class AnthropicErrorResponse(BaseModel):
    type: str = "error"
    error: AnthropicErrorDetail
