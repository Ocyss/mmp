from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class DownloadHistory(BaseModel):
    """
    下载历史记录
    """

    # ID
    id: int
    # 保存路程
    path: str | None = None
    # 类型：电影、电视剧
    type: str | None = None
    # 标题
    title: str | None = None
    # 年份
    year: str | None = None
    # TMDBID
    tmdbid: int | None = None
    # IMDBID
    imdbid: str | None = None
    # TVDBID
    tvdbid: int | None = None
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
    # 季Sxx
    seasons: str | None = None
    # 集Exx
    episodes: str | None = None
    # 背景图
    image: str | None = None
    # 海报
    poster: str | None = None
    # 下载器Hash
    download_hash: str | None = None
    # 种子名称
    torrent_name: str | None = None
    # 种子描述
    torrent_description: str | None = None
    # 站点
    torrent_site: str | None = None
    # 下载用户
    userid: str | None = None
    # 下载用户名
    username: str | None = None
    # 下载渠道
    channel: str | None = None
    # 创建时间
    date: str | None = None
    # 备注
    note: Any | None = None
    # 自定义媒体类别
    media_category: str | None = None
    # 自定义剧集组
    episode_group: str | None = None

    model_config = ConfigDict(from_attributes=True)


class TransferHistory(BaseModel):
    """
    文件整理历史记录
    """

    # ID
    id: int
    # 源目录
    src: str | None = None
    # 目的目录
    dest: str | None = None
    # 转移模式
    mode: str | None = None
    # 类型：电影、电视剧
    type: str | None = None
    # 二级分类
    category: str | None = None
    # 标题
    title: str | None = None
    # 年份
    year: str | None = None
    # TMDBID
    tmdbid: int | None = None
    # IMDBID
    imdbid: str | None = None
    # TVDBID
    tvdbid: int | None = None
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
    # 季Sxx
    seasons: str | None = None
    # 集Exx
    episodes: str | None = None
    # 海报
    image: str | None = None
    # 下载器Hash
    download_hash: str | None = None
    # 自定义剧集组
    episode_group: str | None = None
    # 状态 1-成功，0-失败
    status: bool = True
    # 失败原因
    errmsg: str | None = None
    # 日期
    date: str | None = None

    model_config = ConfigDict(from_attributes=True)


class BatchTransferHistoryRedoRequest(BaseModel):
    history_ids: list[int] = Field(default_factory=list)
