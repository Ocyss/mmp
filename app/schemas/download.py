from typing import Optional

from pydantic import BaseModel, Field


class DownloadTask(BaseModel):
    """
    下载任务
    """

    download_id: str | None = Field(default=None, description="任务ID")
    downloader: str | None = Field(default=None, description="下载器")
    path: str | None = Field(default=None, description="下载路径")
    completed: bool | None = Field(default=False, description="是否完成")


class DownloadDirectory(BaseModel):
    """
    下载目录
    """

    name: str | None = Field(default=None, description="目录名称")
    storage: str | None = Field(default="local", description="存储类型")
    download_path: str | None = Field(default=None, description="配置的下载目录")
    save_path: str | None = Field(default=None, description="可直接传给下载接口 save_path 的路径")
    priority: int | None = Field(default=0, description="目录优先级")
    media_type: str | None = Field(default=None, description="适用媒体类型")
    media_category: str | None = Field(default=None, description="适用媒体分类")
