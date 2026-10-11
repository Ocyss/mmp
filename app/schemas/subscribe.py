from typing import Any, ClassVar, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.schemas.types import MediaType


def compute_subscribe_completed_episode(subscribe: Subscribe) -> int | None:
    """
    计算订阅"已完成"集数派生值，仅用于响应填充，不入库。

    普通电视剧按 ``total_episode - lack_episode`` 计算；分集洗版按订阅目标范围内
    priority==100 的分集数量计算；全集洗版按整包准入基线是否达到 100 计算。
    """
    total_episode = subscribe.total_episode or 0
    if subscribe.type != MediaType.TV.value or not total_episode:
        return None

    start_episode = subscribe.start_episode or 1
    if not subscribe.best_version:
        lack = subscribe.lack_episode or 0
        return max(total_episode - lack, 0)

    if subscribe.best_version_full:
        completed_targets = max(total_episode - start_episode + 1, 0) if subscribe.current_priority == 100 else 0
        return min(min(max(start_episode - 1, 0), total_episode) + completed_targets, total_episode)

    episode_priority = subscribe.episode_priority or {}
    if not episode_priority and subscribe.current_priority is not None:
        # 兼容只有整体优先级的洗版快照，响应派生值需与链路侧按集口径保持一致。
        episode_priority = {str(episode): int(subscribe.current_priority) for episode in range(start_episode, total_episode + 1)}
    priority_completed = sum(
        1
        for ep_key, priority in episode_priority.items()
        if str(ep_key).isdigit() and start_episode <= int(ep_key) <= total_episode and priority == 100
    )
    return min(max(start_episode - 1, 0), total_episode) + priority_completed


class Subscribe(BaseModel):
    # 公共创建和更新接口不得接收系统字段和运行事实；其余字段默认作为订阅输入透传。
    PUBLIC_WRITE_EXCLUDED_FIELDS: ClassVar[frozenset[str]] = frozenset(
        {
            "id",
            "poster",
            "backdrop",
            "vote",
            "description",
            "lack_episode",
            "completed_episode",
            "note",
            "state",
            "last_update",
            "username",
            "current_priority",
            "episode_priority",
            "date",
        }
    )

    id: int | None = None
    # 订阅名称
    name: str | None = None
    # 订阅年份
    year: str | None = None
    # 订阅类型 电影/电视剧
    type: str | None = None
    # 搜索关键字
    keyword: str | None = None
    tmdbid: int | None = None
    doubanid: str | None = None
    bangumiid: int | None = None
    anilistid: int | None = None
    mediaid: str | None = None
    media_source: str | None = None
    media_id: str | None = None
    # 季号
    season: int | None = None
    # 海报
    poster: str | None = None
    # 背景图
    backdrop: str | None = None
    # 评分
    vote: float | None = 0.0
    # 描述
    description: str | None = None
    # 过滤规则
    filter: str | None = None
    # 包含
    include: str | None = None
    # 排除
    exclude: str | None = None
    # 质量
    quality: str | None = None
    # 分辨率
    resolution: str | None = None
    # 特效
    effect: str | None = None
    # 总集数
    total_episode: int | None = 0
    # 开始集数
    start_episode: int | None = 0
    # 缺失集数
    lack_episode: int | None = 0
    # 已完成集数
    completed_episode: int | None = None
    # 附加信息
    note: Any | None = None
    # 状态：N-新建， R-订阅中
    state: str | None = None
    # 最后更新时间
    last_update: str | None = None
    # 订阅用户
    username: str | None = None
    # 订阅站点
    sites: list[int] | None = Field(default_factory=list)
    # 下载器
    downloader: str | None = None
    # 是否洗版
    best_version: int | None = None
    # 是否只洗全集整包
    best_version_full: int | None = None
    # 当前优先级
    current_priority: int | None = None
    # 洗版时已下载剧集的优先级状态
    episode_priority: dict[str, int] | None = None
    # 保存路径
    save_path: str | None = None
    # 是否使用 imdbid 搜索
    search_imdbid: int | None = 0
    # 时间
    date: str | None = None
    # 自定义识别词
    custom_words: str | None = None
    # 自定义媒体类别
    media_category: str | None = None
    # 过滤规则组
    filter_groups: list[str] | None = Field(default_factory=list)
    # 剧集组
    episode_group: str | None = None

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def _fill_completed_episode(self) -> Subscribe:
        """
        填充 ``completed_episode`` 派生字段。电视剧订阅按 best_version 分支计算，
        电影或缺少 total_episode 时保持 None。
        """
        if self.completed_episode is not None:
            # 调用方显式提供过的值不覆盖
            return self
        self.completed_episode = compute_subscribe_completed_episode(self)
        return self

    def to_public_write_payload(self) -> dict[str, Any]:
        """裁剪公共订阅写入字段，避免请求体覆盖下载事实和运行状态。"""
        return self.model_dump(exclude=self.PUBLIC_WRITE_EXCLUDED_FIELDS)


class SubscribeShare(BaseModel):
    # 分享ID
    id: int | None = None
    # 订阅ID
    subscribe_id: int | None = None
    # 分享标题
    share_title: str | None = None
    # 分享说明
    share_comment: str | None = None
    # 分享人
    share_user: str | None = None
    # 分享人唯一ID
    share_uid: str | None = None
    # 订阅名称
    name: str | None = None
    # 订阅年份
    year: str | None = None
    # 订阅类型 电影/电视剧
    type: str | None = None
    # 搜索关键字
    keyword: str | None = None
    tmdbid: int | None = None
    doubanid: str | None = None
    bangumiid: int | None = None
    anilistid: int | None = None
    media_source: str | None = None
    media_id: str | None = None
    # 季号
    season: int | None = None
    # 海报
    poster: str | None = None
    # 背景图
    backdrop: str | None = None
    # 评分
    vote: float | None = 0.0
    # 描述
    description: str | None = None
    # 包含
    include: str | None = None
    # 排除
    exclude: str | None = None
    # 质量
    quality: str | None = None
    # 分辨率
    resolution: str | None = None
    # 特效
    effect: str | None = None
    # 总集数
    total_episode: int | None = 0
    # 时间
    date: str | None = None
    # 自定义识别词
    custom_words: str | None = None
    # 自定义媒体类别
    media_category: str | None = None
    # 自定义剧集组
    episode_group: str | None = None
    # 复用人次
    count: int | None = 0


class SubscribeShareStatistics(BaseModel):
    # 分享人
    share_user: str | None = None
    # 分享数量
    share_count: int | None = 0
    # 总复用人次
    total_reuse_count: int | None = 0


class SubscribeDownloadFileInfo(BaseModel):
    # 种子名称
    torrent_title: str | None = None
    # 站点名称
    site_name: str | None = None
    # 下载器
    downloader: str | None = None
    # hash
    hash: str | None = None
    # 文件路径
    file_path: str | None = None


class SubscribeLibraryFileInfo(BaseModel):
    # 存储
    storage: str | None = "local"
    # 文件路径
    file_path: str | None = None
    # 媒体服务器名称
    server: str | None = None
    # 媒体服务器类型：emby、jellyfin、plex 等
    server_type: str | None = None
    # 媒体服务器条目 ID
    itemid: str | None = None


class SubscribeEpisodeInfo(BaseModel):
    # 标题
    title: str | None = None
    # 描述
    description: str | None = None
    # 背景图
    backdrop: str | None = None
    # 下载文件信息
    download: list[SubscribeDownloadFileInfo] | None = Field(default_factory=list)
    # 媒体库文件信息
    library: list[SubscribeLibraryFileInfo] | None = Field(default_factory=list)


class SubscrbieInfo(BaseModel):
    # 订阅信息
    subscribe: Subscribe | None = None
    # 集信息 {集号: {download: 文件路径，library: 文件路径, backdrop: url, title: 标题, description: 描述}}
    episodes: dict[int, SubscribeEpisodeInfo] | None = Field(default_factory=dict)
