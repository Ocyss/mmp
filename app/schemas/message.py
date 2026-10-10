from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Union

from pydantic import BaseModel, Field, field_validator

from app.schemas.types import ContentType, MessageChannel, NotificationType


class NotificationClearScope(str, Enum):
    """
    通知中心清理范围。
    """

    # 全部消息
    All = "all"
    # 系统消息
    System = "system"
    # 媒体消息
    Media = "media"


class NotificationClearBefore(BaseModel):
    """
    通知中心按范围记录的清理时间。
    """

    # 全部消息清理时间
    all: int = 0
    # 系统消息清理时间
    system: int = 0
    # 媒体消息清理时间
    media: int = 0


class MessageResponse(BaseModel):
    """
    消息发送响应，包含消息ID等信息用于后续编辑
    """

    # 消息ID
    message_id: str | int | None = None
    # 聊天ID
    chat_id: str | int | None = None
    # 消息渠道
    channel: MessageChannel | None = None
    # 消息来源
    source: str | None = None
    # 渠道自定义上下文（如飞书流式卡片 card_id/element_id/sequence）
    metadata: dict[str, Any] | None = None
    # 是否发送成功
    success: bool = False


class NotificationHistoryItem(BaseModel):
    """
    通知历史记录。
    """

    # 消息ID
    id: int | None = None
    # 消息渠道
    channel: str | None = None
    # 消息来源
    source: str | None = None
    # 消息类型
    mtype: str | None = None
    # 标题
    title: str | None = None
    # 文本内容
    text: str | None = None
    # 图片
    image: str | None = None
    # 链接
    link: str | None = None
    # 用户ID
    userid: str | None = None
    # 登记时间
    reg_time: str | None = None
    # 消息方向：0-接收消息，1-发送消息
    action: int | None = None
    # 附件json
    note: list | dict | None = None


class CommingMessage(BaseModel):
    """
    外来消息
    """

    class MessageImage(BaseModel):
        """
        外来消息图片
        """

        ref: str
        name: str | None = None
        mime_type: str | None = None
        size: int | None = None

        @classmethod
        def from_value(cls, value: Any) -> CommingMessage.MessageImage | None:
            if value is None:
                return None
            if isinstance(value, cls):
                return value
            if isinstance(value, str):
                return cls(ref=value)
            if isinstance(value, dict):
                ref = value.get("ref") or value.get("url") or value.get("image_url") or value.get("file_url")
                if not ref:
                    return None
                size = value.get("size")
                try:
                    size = int(size) if size is not None else None
                except TypeError, ValueError:
                    size = None
                return cls(
                    ref=ref,
                    name=value.get("name") or value.get("filename"),
                    mime_type=value.get("mime_type") or value.get("content_type"),
                    size=size,
                )
            return None

        @classmethod
        def normalize_list(cls, values: Any | None) -> list[CommingMessage.MessageImage] | None:
            if not values:
                return None
            if not isinstance(values, list):
                values = [values]
            normalized = []
            for value in values:
                item = cls.from_value(value)
                if item:
                    normalized.append(item)
            return normalized or None

    class MessageAttachment(BaseModel):
        """
        外来消息附件（非图片/非语音）
        """

        ref: str
        name: str | None = None
        mime_type: str | None = None
        size: int | None = None

    # 用户ID
    userid: str | int | None = None
    # 用户名称
    username: str | int | None = None
    # 消息渠道
    channel: MessageChannel | None = None
    # 来源（渠道名称）
    source: str | None = None
    # 消息体
    text: str | None = None
    # 时间
    date: str | None = None
    # 消息方向
    action: int | None = 0
    # 是否为回调消息
    is_callback: bool | None = False
    # 回调数据
    callback_data: str | None = None
    # 消息ID（用于回调时定位原消息）
    message_id: str | int | None = None
    # 聊天ID（用于回调时定位聊天）
    chat_id: str | None = None
    # 回复目标消息ID（用于 ForceReply 等回复场景）
    reply_to_message_id: str | int | None = None
    # 完整的回调查询信息（原始数据）
    callback_query: dict | None = None
    # 图片列表（图片URL或file_id）
    images: list[MessageImage] | None = None
    # 语音/音频引用列表
    audio_refs: list[str] | None = None
    # 文件附件列表
    files: list[MessageAttachment] | None = None

    @field_validator("images", mode="before")
    @classmethod
    def _normalize_images(cls, value: Any) -> list[CommingMessage.MessageImage] | None:
        return cls.MessageImage.normalize_list(value)

    def to_dict(self):
        """
        转换为字典
        """
        items = self.model_dump()
        for k, v in items.items():
            if isinstance(v, MessageChannel):
                items[k] = v.value
        return items


class Notification(BaseModel):
    """
    消息
    """

    # 消息渠道
    channel: MessageChannel | None = None
    # 消息来源
    source: str | None = None
    # 消息类型
    mtype: NotificationType | None = None
    # 内容类型
    ctype: ContentType | None = None
    # 标题
    title: str | None = None
    # 文本内容
    text: str | None = None
    # 图片
    image: str | None = None
    # 语音文件路径
    voice_path: str | None = None
    # 本地文件路径
    file_path: str | None = None
    # 发送时展示的文件名
    file_name: str | None = None
    # 语音消息附带说明文字
    voice_caption: str | None = None
    # 链接
    link: str | None = None
    # 用户ID
    userid: str | int | None = None
    # 用户名称
    username: str | int | None = None
    # 时间
    date: str | None = None
    # 消息方向
    action: int | None = 1
    # 消息目标用户ID字典，未指定用户ID时使用
    targets: dict | None = None
    # 按钮列表，格式：[[{"text": "按钮文本", "callback_data": "回调数据", "url": "链接"}]]
    buttons: list[list[dict]] | None = None
    # Telegram ForceReply 回复标记
    force_reply: bool = False
    # 原消息ID，用于编辑消息
    original_message_id: str | int | None = None
    # 原消息的聊天ID，用于编辑消息
    original_chat_id: str | None = None
    # 是否禁用链接预览（仅Telegram支持）
    disable_web_page_preview: bool | None = None
    # Telegram 消息格式类型，默认 MarkdownV2，可传 HTML
    parse_mode: str | None = None
    # 是否写入消息历史
    save_history: bool = True

    def to_dict(self):
        """
        转换为字典
        """
        items = self.model_dump()
        for k, v in items.items():
            if isinstance(v, MessageChannel) or isinstance(v, NotificationType):
                items[k] = v.value
        return items


class NotificationSwitch(BaseModel):
    """
    消息开关
    """

    # 消息类型
    mtype: str | None = None
    # 微信开关
    wechat: bool | None = False
    # 飞书开关
    feishu: bool | None = False
    # TG开关
    telegram: bool | None = False
    # Slack开关
    slack: bool | None = False
    # SynologyChat开关
    synologychat: bool | None = False
    # VoceChat开关
    vocechat: bool | None = False
    # WebPush开关
    webpush: bool | None = False
    # QQ开关
    qq: bool | None = False


class Subscription(BaseModel):
    """
    客户端消息订阅
    """

    endpoint: str | None = None
    keys: dict | None = Field(default_factory=dict)


class SubscriptionMessage(BaseModel):
    """
    客户端订阅消息体
    """

    title: str | None = None
    body: str | None = None
    icon: str | None = None
    url: str | None = None
    data: dict | None = Field(default_factory=dict)


class AgentWebChatRequest(BaseModel):
    """
    Web 智能助手对话请求。
    """

    class AgentWebChatFile(BaseModel):
        """
        Web 智能助手输入附件。
        """

        ref: str = Field(..., min_length=1)
        name: str | None = Field(None)
        mime_type: str | None = Field(None)
        size: int | None = Field(None)
        local_path: str | None = Field(None)
        status: str | None = Field(None)

    # 用户本轮输入
    text: str = Field(default="")
    # 展示历史中记录的用户可读文本；为空时使用 text
    display_text: str | None = Field(None)
    # 前端会话标识，相同标识复用同一段 Agent 记忆
    session_id: str | None = Field(None)
    # 图片 URL 或 data URL 列表
    images: list[str] | None = Field(default_factory=list)
    # 语音/音频引用列表
    audio_refs: list[str] | None = Field(default_factory=list)
    # 文件附件列表
    files: list[AgentWebChatFile] | None = Field(default_factory=list)
    # 用户通过按钮选择时的完整选择快照
    choice_selection: dict[str, Any] | None = Field(default=None)
    # WebAgent 按钮回调关联的原消息 ID，用于传统交互原地编辑卡片
    original_message_id: str | int | None = Field(default=None)
    # WebAgent 按钮回调关联的原聊天 ID，用于传统交互原地编辑卡片
    original_chat_id: str | int | None = Field(default=None)
    # 是否在展示历史中记录本轮用户消息
    echo_user: bool = Field(default=True)


class AgentWebChoiceRequest(BaseModel):
    """
    Web 智能助手按钮选择请求。
    """

    # 前端会话标识，用于保持与原对话窗口的关联
    session_id: str | None = Field(None)
    # Agent 工具生成的按钮回调数据
    callback_data: str = Field(..., min_length=1)
    # WebAgent 原助手消息 ID，用于传统按钮回调原地编辑
    original_message_id: str | int | None = Field(default=None)
    # WebAgent 原聊天 ID，用于传统按钮回调原地编辑
    original_chat_id: str | int | None = Field(default=None)


class ChannelCapability(Enum):
    """
    渠道能力枚举
    """

    # 支持内联按钮
    INLINE_BUTTONS = "inline_buttons"
    # 支持菜单命令
    MENU_COMMANDS = "menu_commands"
    # 支持消息编辑
    MESSAGE_EDITING = "message_editing"
    # 支持消息删除
    MESSAGE_DELETION = "message_deletion"
    # 支持回调查询
    CALLBACK_QUERIES = "callback_queries"
    # 支持富文本
    RICH_TEXT = "rich_text"
    # 支持 Markdown
    MARKDOWN = "markdown"
    # 支持图片
    IMAGES = "images"
    # 支持链接
    LINKS = "links"
    # 支持原生语音输出
    AUDIO_OUTPUT = "audio_output"
    # 支持文件发送
    FILE_SENDING = "file_sending"
    # 支持可收口的消息处理状态提示，如 reaction 或 typing
    PROCESSING_STATUS = "processing_status"


@dataclass
class ChannelCapabilities:
    """
    渠道能力配置
    """

    channel: MessageChannel
    capabilities: set[ChannelCapability]
    max_buttons_per_row: int = 5
    max_button_rows: int = 10
    max_button_text_length: int = 30
    # 单条消息最大长度（0 表示不限制），用于流式输出时自动分段
    max_message_length: int = 0
    fallback_enabled: bool = True


class ChannelCapabilityManager:
    """
    渠道能力管理器
    """

    _capabilities: dict[MessageChannel, ChannelCapabilities] = {
        MessageChannel.Telegram: ChannelCapabilities(
            channel=MessageChannel.Telegram,
            capabilities={
                ChannelCapability.INLINE_BUTTONS,
                ChannelCapability.MENU_COMMANDS,
                ChannelCapability.MESSAGE_EDITING,
                ChannelCapability.MESSAGE_DELETION,
                ChannelCapability.CALLBACK_QUERIES,
                ChannelCapability.MARKDOWN,
                ChannelCapability.RICH_TEXT,
                ChannelCapability.IMAGES,
                ChannelCapability.LINKS,
                ChannelCapability.AUDIO_OUTPUT,
                ChannelCapability.FILE_SENDING,
                ChannelCapability.PROCESSING_STATUS,
            },
            max_buttons_per_row=4,
            max_button_rows=10,
            max_button_text_length=30,
            # Telegram 文本消息限制 4096 字符，预留空间给 MarkdownV2 转义和标题
            max_message_length=3500,
        ),
        MessageChannel.Wechat: ChannelCapabilities(
            channel=MessageChannel.Wechat,
            capabilities={
                ChannelCapability.IMAGES,
                ChannelCapability.LINKS,
                ChannelCapability.AUDIO_OUTPUT,
                ChannelCapability.MENU_COMMANDS,
            },
            fallback_enabled=True,
        ),
        MessageChannel.Feishu: ChannelCapabilities(
            channel=MessageChannel.Feishu,
            capabilities={
                ChannelCapability.INLINE_BUTTONS,
                ChannelCapability.MESSAGE_EDITING,
                ChannelCapability.CALLBACK_QUERIES,
                ChannelCapability.MARKDOWN,
                ChannelCapability.RICH_TEXT,
                ChannelCapability.IMAGES,
                ChannelCapability.LINKS,
                ChannelCapability.AUDIO_OUTPUT,
                ChannelCapability.FILE_SENDING,
                ChannelCapability.PROCESSING_STATUS,
            },
            max_buttons_per_row=3,
            max_button_rows=8,
            max_button_text_length=20,
            max_message_length=30000,
            fallback_enabled=True,
        ),
        MessageChannel.WechatClawBot: ChannelCapabilities(
            channel=MessageChannel.WechatClawBot,
            capabilities={
                ChannelCapability.MARKDOWN,
                ChannelCapability.IMAGES,
                ChannelCapability.LINKS,
                ChannelCapability.FILE_SENDING,
            },
            max_message_length=2800,
            fallback_enabled=True,
        ),
        MessageChannel.Slack: ChannelCapabilities(
            channel=MessageChannel.Slack,
            capabilities={
                ChannelCapability.INLINE_BUTTONS,
                ChannelCapability.MESSAGE_EDITING,
                ChannelCapability.MESSAGE_DELETION,
                ChannelCapability.CALLBACK_QUERIES,
                ChannelCapability.MARKDOWN,
                ChannelCapability.RICH_TEXT,
                ChannelCapability.IMAGES,
                ChannelCapability.LINKS,
                ChannelCapability.MENU_COMMANDS,
                ChannelCapability.FILE_SENDING,
                ChannelCapability.PROCESSING_STATUS,
            },
            max_buttons_per_row=3,
            max_button_rows=8,
            max_button_text_length=25,
            # Slack 消息限制 40000 字符，预留空间给格式化
            max_message_length=39000,
            fallback_enabled=True,
        ),
        MessageChannel.Discord: ChannelCapabilities(
            channel=MessageChannel.Discord,
            capabilities={
                ChannelCapability.INLINE_BUTTONS,
                ChannelCapability.MESSAGE_EDITING,
                ChannelCapability.MESSAGE_DELETION,
                ChannelCapability.CALLBACK_QUERIES,
                ChannelCapability.MARKDOWN,
                ChannelCapability.RICH_TEXT,
                ChannelCapability.IMAGES,
                ChannelCapability.LINKS,
                ChannelCapability.FILE_SENDING,
                ChannelCapability.PROCESSING_STATUS,
            },
            max_buttons_per_row=5,
            max_button_rows=5,
            max_button_text_length=80,
            # Discord 消息限制 2000 字符
            max_message_length=1800,
            fallback_enabled=True,
        ),
        MessageChannel.SynologyChat: ChannelCapabilities(
            channel=MessageChannel.SynologyChat,
            capabilities={
                ChannelCapability.MARKDOWN,
                ChannelCapability.RICH_TEXT,
                ChannelCapability.IMAGES,
                ChannelCapability.LINKS,
            },
            fallback_enabled=True,
        ),
        MessageChannel.VoceChat: ChannelCapabilities(
            channel=MessageChannel.VoceChat,
            capabilities={
                ChannelCapability.MARKDOWN,
                ChannelCapability.RICH_TEXT,
                ChannelCapability.IMAGES,
                ChannelCapability.LINKS,
            },
            fallback_enabled=True,
        ),
        MessageChannel.WebPush: ChannelCapabilities(
            channel=MessageChannel.WebPush,
            capabilities={ChannelCapability.LINKS},
            fallback_enabled=True,
        ),
        MessageChannel.Web: ChannelCapabilities(
            channel=MessageChannel.Web,
            capabilities={
                ChannelCapability.MARKDOWN,
                ChannelCapability.RICH_TEXT,
                ChannelCapability.IMAGES,
                ChannelCapability.LINKS,
            },
            fallback_enabled=True,
        ),
        MessageChannel.WebAgent: ChannelCapabilities(
            channel=MessageChannel.WebAgent,
            capabilities={
                ChannelCapability.INLINE_BUTTONS,
                ChannelCapability.CALLBACK_QUERIES,
                ChannelCapability.MESSAGE_EDITING,
                ChannelCapability.MARKDOWN,
                ChannelCapability.RICH_TEXT,
                ChannelCapability.IMAGES,
                ChannelCapability.LINKS,
                ChannelCapability.AUDIO_OUTPUT,
                ChannelCapability.FILE_SENDING,
            },
            fallback_enabled=False,
        ),
        MessageChannel.QQ: ChannelCapabilities(
            channel=MessageChannel.QQ,
            capabilities={
                ChannelCapability.RICH_TEXT,
                ChannelCapability.IMAGES,
                ChannelCapability.LINKS,
                ChannelCapability.INLINE_BUTTONS,
                ChannelCapability.CALLBACK_QUERIES,
            },
            max_buttons_per_row=5,
            max_button_rows=5,
            max_button_text_length=30,
            fallback_enabled=True,
        ),
    }

    @classmethod
    def get_capabilities(cls, channel: MessageChannel) -> ChannelCapabilities | None:
        """
        获取渠道能力
        """
        return cls._capabilities.get(channel)

    @classmethod
    def supports_capability(cls, channel: MessageChannel, capability: ChannelCapability) -> bool:
        """
        检查渠道是否支持某项能力
        """
        channel_caps = cls.get_capabilities(channel)
        if not channel_caps:
            return False
        return capability in channel_caps.capabilities

    @classmethod
    def supports_buttons(cls, channel: MessageChannel) -> bool:
        """
        检查渠道是否支持按钮
        """
        return cls.supports_capability(channel, ChannelCapability.INLINE_BUTTONS)

    @classmethod
    def supports_callbacks(cls, channel: MessageChannel) -> bool:
        """
        检查渠道是否支持回调
        """
        return cls.supports_capability(channel, ChannelCapability.CALLBACK_QUERIES)

    @classmethod
    def supports_editing(cls, channel: MessageChannel) -> bool:
        """
        检查渠道是否支持消息编辑
        """
        return cls.supports_capability(channel, ChannelCapability.MESSAGE_EDITING)

    @classmethod
    def supports_markdown(cls, channel: MessageChannel) -> bool:
        """
        检查渠道是否支持 Markdown。
        """
        return cls.supports_capability(channel, ChannelCapability.MARKDOWN)

    @classmethod
    def supports_deletion(cls, channel: MessageChannel) -> bool:
        """
        检查渠道是否支持消息删除
        """
        return cls.supports_capability(channel, ChannelCapability.MESSAGE_DELETION)

    @classmethod
    def get_max_buttons_per_row(cls, channel: MessageChannel) -> int:
        """
        获取每行最大按钮数
        """
        channel_caps = cls.get_capabilities(channel)
        return channel_caps.max_buttons_per_row if channel_caps else 2

    @classmethod
    def get_max_button_rows(cls, channel: MessageChannel) -> int:
        """
        获取最大按钮行数
        """
        channel_caps = cls.get_capabilities(channel)
        return channel_caps.max_button_rows if channel_caps else 5

    @classmethod
    def get_max_button_text_length(cls, channel: MessageChannel) -> int:
        """
        获取按钮文本最大长度
        """
        channel_caps = cls.get_capabilities(channel)
        return channel_caps.max_button_text_length if channel_caps else 20

    @classmethod
    def get_max_message_length(cls, channel: MessageChannel) -> int:
        """
        获取单条消息最大长度（0 表示不限制）
        """
        channel_caps = cls.get_capabilities(channel)
        return channel_caps.max_message_length if channel_caps else 0

    @classmethod
    def should_use_fallback(cls, channel: MessageChannel) -> bool:
        """
        是否应该使用降级策略
        """
        channel_caps = cls.get_capabilities(channel)
        return channel_caps.fallback_enabled if channel_caps else True
