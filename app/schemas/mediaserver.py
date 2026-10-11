from typing import TYPE_CHECKING, Any, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from pathlib import Path

    from app.schemas.types import MediaType


class ExistMediaInfo(BaseModel):
    """
    媒体服务器存在媒体信息
    """

    # 类型 电影、电视剧
    type: MediaType | None = None
    # 季
    seasons: dict[int, list] | None = Field(default_factory=dict)
    # 媒体服务器类型：plex、jellyfin、emby、zspace、trimemedia、ugreen
    server_type: str | None = None
    # 媒体服务器名称
    server: str | None = None
    # 媒体ID
    itemid: str | int | None = None


class NotExistMediaInfo(BaseModel):
    """
    媒体服务器不存在媒体信息
    """

    # 季
    season: int | None = None
    # 剧集列表
    episodes: list | None = Field(default_factory=list)
    # 总集数
    total_episode: int | None = 0
    # 开始集
    start_episode: int | None = 0
    # 候选资源须完整覆盖目标范围
    require_complete_coverage: bool | None = False


class RefreshMediaItem(BaseModel):
    """
    媒体库刷新信息
    """

    # 标题
    title: str | None = None
    # 年份
    year: str | int | None = None
    # 类型
    type: MediaType | None = None
    # 类别
    category: str | None = None
    # 目录
    target_path: Path | None = None


class MediaServerLibrary(BaseModel):
    """
    媒体服务器媒体库信息
    """

    # 服务器
    server: str | None = None
    # ID
    id: str | int | None = None
    # 媒体服务器项目ID
    item_id: str | int | None = None
    # 媒体服务器ID
    server_id: str | None = None
    # 名称
    name: str | None = None
    # 路径
    path: str | list | None = None
    # 类型
    type: str | None = None
    # 媒体库内媒体数量
    item_count: int | None = None
    # 封面图
    image: str | None = None
    # 封面图列表
    image_list: list[str] | None = None
    # 跳转链接
    link: str | None = None
    # 服务器类型
    server_type: str | None = None
    # 飞牛的图片需要Cookies
    use_cookies: bool | None = None


class MediaServerItemUserState(BaseModel):
    # 已播放
    played: bool | None = None
    # 继续播放
    resume: bool | None = None
    # 上次播放时间 10位时间戳
    last_played_date: str | None = None
    # 播放次数(不等于完播次数，理解为浏览次数)
    play_count: int | None = None
    # 播放进度
    percentage: float | None = None


class MediaServerItem(BaseModel):
    """
    媒体服务器媒体信息
    """

    # ID
    id: str | int | None = None
    # 服务器
    server: str | None = None
    # 媒体库ID
    library: str | int | None = None
    # 媒体服务器ID
    server_id: str | None = None
    # ID
    item_id: str | None = None
    # 类型
    item_type: str | None = None
    # 标题
    title: str | None = None
    # 原标题
    original_title: str | None = None
    # 年份
    year: str | int | None = None
    # TMDBID
    tmdbid: int | None = None
    # IMDBID
    imdbid: str | None = None
    # TVDBID
    tvdbid: str | None = None
    # 路径
    path: str | None = None
    # 季集
    seasoninfo: dict[int, list] | None = None
    # 备注
    note: Any | None = None
    # 同步时间
    lst_mod_date: str | None = None
    user_state: MediaServerItemUserState | None = None

    model_config = ConfigDict(from_attributes=True)


class MediaServerSeasonInfo(BaseModel):
    """
    媒体服务器媒体剧集信息
    """

    season: int | None = None
    episodes: list[int] | None = Field(default_factory=list)


class WebhookEventInfo(BaseModel):
    """
    Webhook事件信息
    """

    event: str | None = None
    channel: str | None = None
    server_name: str | None = None
    item_type: str | None = None
    item_name: str | None = None
    item_id: str | None = None
    item_path: str | None = None
    season_id: str | None = None
    episode_id: str | None = None
    tmdb_id: str | None = None
    overview: str | None = None
    percentage: float | None = None
    ip: str | None = None
    device_name: str | None = None
    client: str | None = None
    user_name: str | None = None
    image_url: str | None = None
    item_favorite: bool | None = None
    save_reason: str | None = None
    item_isvirtual: bool | None = None
    media_type: str | None = None
    json_object: dict | None = Field(default_factory=dict)


class MediaServerPlayItem(BaseModel):
    """
    媒体服务器可播放项目信息
    """

    id: str | int | None = None
    item_id: str | int | None = None
    server_id: str | None = None
    title: str | None = None
    subtitle: str | None = None
    type: str | None = None
    image: str | None = None
    link: str | None = None
    percent: float | None = None
    BackdropImageTags: list | None = Field(default_factory=list)
    server_type: str | None = None
    # 飞牛的图片需要Cookies
    use_cookies: bool | None = None
