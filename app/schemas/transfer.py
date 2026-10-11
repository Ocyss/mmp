from typing import TYPE_CHECKING, Any, Optional

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

    from app.schemas.context import MediaInfo, MetaInfo
    from app.schemas.file import FileItem
    from app.schemas.history import DownloadHistory
    from app.schemas.system import TransferDirectoryConf
    from app.schemas.tmdb import TmdbEpisode


class DownloaderTorrent(BaseModel):
    """
    下载器任务信息
    """

    downloader: str | None = None
    hash: str | None = None
    title: str | None = None
    site_name: str | None = None
    name: str | None = None
    year: str | None = None
    season_episode: str | None = None
    path: Path | None = None
    size: float | None = 0.0
    progress: float | None = 0.0
    state: str | None = "downloading"
    upspeed: str | None = None
    dlspeed: str | None = None
    tags: str | None = None
    save_path: str | None = None
    content_path: str | None = None
    category: str | None = None
    download_limit: float | None = None
    upload_limit: float | None = None
    ratio_limit: float | None = None
    seeding_time_limit: int | None = None
    trackers: list[str] | None = Field(default_factory=list)
    media: dict | None = Field(default_factory=dict)
    userid: str | None = None
    username: str | None = None
    left_time: str | None = None


class TransferTorrent(DownloaderTorrent):
    """
    待转移任务信息
    """


class DownloadingTorrent(DownloaderTorrent):
    """
    下载中任务信息
    """


class TransferTask(BaseModel):
    """
    文件整理任务
    """

    fileitem: FileItem
    meta: Any | None = None
    mediainfo: Any | None = None
    media_source: str | None = None
    target_directory: TransferDirectoryConf | None = None
    target_storage: str | None = None
    target_path: Path | None = None
    transfer_type: str | None = None
    scrape: bool | None = False
    library_type_folder: bool | None = False
    library_category_folder: bool | None = False
    episodes_info: list[TmdbEpisode] | None = None
    username: str | None = None
    downloader: str | None = None
    download_hash: str | None = None
    download_history: DownloadHistory | None = None
    transfer_batch_id: str | None = None
    manual: bool | None = False
    background: bool | None = True
    preview: bool | None = False

    def to_dict(self):
        """
        返回字典
        """
        dicts = vars(self).copy()
        dicts["fileitem"] = self.fileitem.model_dump() if self.fileitem else None
        dicts["meta"] = self.meta.model_dump() if self.meta else None
        dicts["mediainfo"] = self.mediainfo.model_dump() if self.mediainfo else None
        dicts["target_directory"] = self.target_directory.model_dump() if self.target_directory else None
        return dicts


class TransferJobTask(BaseModel):
    """
    文件整理作业任务
    """

    fileitem: FileItem | None = None
    meta: MetaInfo | None = None
    state: str | None = None
    downloader: str | None = None
    download_hash: str | None = None


class TransferJob(BaseModel):
    """
    文件整理作业
    """

    media: MediaInfo | None = None
    season: int | None = None
    tasks: list[TransferJobTask] | None = Field(default_factory=list)


class TransferInfo(BaseModel):
    """
    文件整理结果
    """

    # 是否成功标志
    success: bool = True
    # 整理⼁路径
    fileitem: FileItem | None = None
    # 转移后的目录项，媒体的根目录
    target_diritem: FileItem | None = None
    # 转移后路径
    target_item: FileItem | None = None
    # 整理方式
    transfer_type: str | None = None
    # 处理文件数
    file_count: int | None = Field(default=0)
    # 处理文件清单
    file_list: list | None = Field(default_factory=list)
    # 目标文件清单
    file_list_new: list | None = Field(default_factory=list)
    # 总文件大小
    total_size: int | None = Field(default=0)
    # 失败清单
    fail_list: list | None = Field(default_factory=list)
    # 错误信息
    message: str | None = None
    # 是否需要刮削
    need_scrape: bool | None = False
    # 是否需要通知
    need_notify: bool | None = False

    def to_dict(self):
        """
        返回字典
        """
        dicts = vars(self).copy()
        dicts["fileitem"] = self.fileitem.model_dump() if self.fileitem else None
        dicts["target_item"] = self.target_item.model_dump() if self.target_item else None
        return dicts


class TransferQueue(BaseModel):
    """
    异步整理队列信息
    """

    # 任务信息
    task: TransferTask | None = None
    # 回调函数
    callback: Callable | None = None
    # 整理结果
    result: TransferInfo | None = None


class EpisodeFormat(BaseModel):
    """
    剧集自定义识别格式
    """

    format: str | None = None
    detail: str | None = None
    part: str | None = None
    offset: str | None = None


class EpisodeFormatRule(BaseModel):
    """
    集数定位规则
    """

    name: str
    enabled: bool = True
    order: int = 0
    pattern: str
    min_file_size_mb: int = 0


class EpisodeFormatRecommendItem(BaseModel):
    """
    集数定位推荐请求
    """

    fileitem: FileItem | None = None
    fileitems: list[FileItem] | None = None


class ManualTransferItem(BaseModel):
    """
    手动整理请求，兼容历史数据源ID字段并支持统一来源与原生ID
    """

    # 文件项
    fileitem: FileItem = None
    # 文件项列表（前端多选时传入）
    fileitems: list[FileItem] | None = None
    # 日志ID
    logid: int | None = None
    # 日志ID列表（前端多选历史记录时传入）
    logids: list[int] | None = None
    # 目标存储
    target_storage: str | None = None
    # 目标路径
    target_path: str | None = None
    # TMDB ID
    tmdbid: int | None = None
    # 豆瓣ID
    doubanid: str | None = None
    # Bangumi ID
    bangumiid: int | None = None
    # AniList ID
    anilistid: int | None = None
    # 媒体数据源
    media_source: str | None = None
    # 数据源原生ID
    media_id: str | None = None
    # 类型
    type_name: str | None = None
    # 季号
    season: int | None = None
    # 整理方式
    transfer_type: str | None = None
    # 自定义格式
    episode_format: str | None = None
    # 指定集数
    episode_detail: str | None = None
    # 指定PART
    episode_part: str | None = None
    # 集数偏移
    episode_offset: str | None = None
    # 最小文件大小
    min_filesize: int | None = 0
    # 刮削
    scrape: bool | None = False
    # 媒体库类型子目录
    library_type_folder: bool | None = None
    # 媒体库类别子目录
    library_category_folder: bool | None = None
    # 复用历史识别信息
    from_history: bool | None = False
    # 剧集组
    episode_group: str | None = None
    # 仅预览，不执行整理
    preview: bool | None = False
    # 重新整理，清理命中的成功历史及其旧目标
    reorganize: bool | None = False


class ManualTransferHistoryInfo(BaseModel):
    """
    手动整理命中的成功历史摘要
    """

    # 是否应显示重新整理操作
    reorganize: bool = False
    # 命中的成功历史数量
    history_count: int = 0


class ManualTransferTargetPath(BaseModel):
    """
    手动整理目的路径匹配结果
    """

    # 目标存储
    target_storage: str | None = None
    # 目标路径
    target_path: str | None = None
    # 整理方式
    transfer_type: str | None = None
    # 刮削
    scrape: bool | None = False
    # 媒体库类型子目录
    library_type_folder: bool | None = False
    # 媒体库类别子目录
    library_category_folder: bool | None = False
