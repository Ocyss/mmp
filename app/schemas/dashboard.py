from typing import Optional

from pydantic import BaseModel, Field, model_validator

from app.helper.locale import LocaleHelper


class Statistic(BaseModel):
    """媒体库数量统计。"""

    # 电影
    movie_count: int | None = 0
    # 电视剧数量
    tv_count: int | None = 0
    # 集数量
    episode_count: int | None = 0
    # 用户数量
    user_count: int | None = 0
    # 本月新增电影数量
    movie_count_month: int | None = 0
    # 本月新增电视剧数量
    tv_count_month: int | None = 0
    # 本月新增剧集数量
    episode_count_month: int | None = 0


class Storage(BaseModel):
    """仪表板存储空间统计。"""

    # 总存储空间
    total_storage: float | None = 0.0
    # 已使用空间
    used_storage: float | None = 0.0


class ProcessInfo(BaseModel):
    """仪表板进程运行信息。"""

    # 进程ID
    pid: int | None = 0
    # 进程名称
    name: str | None = None
    # 进程状态
    status: str | None = None
    # 进程占用CPU
    cpu: float | None = 0.0
    # 进程占用内存 MB
    memory: float | None = 0.0
    # 进程创建时间
    create_time: float | None = 0.0
    # 进程运行时间 秒
    run_time: float | None = 0.0


class DownloaderInfo(BaseModel):
    """仪表板下载器汇总信息。"""

    # 下载速度
    download_speed: float | None = 0.0
    # 上传速度
    upload_speed: float | None = 0.0
    # 下载量
    download_size: float | None = 0.0
    # 上传量
    upload_size: float | None = 0.0
    # 剩余空间
    free_space: float | None = 0.0


class DashboardMemoryInfo(BaseModel):
    """仪表板应用进程与系统内存统计。"""

    # 总内存字节数
    total: int = 0
    # 当前 MoviePilot 进程使用内存字节数
    used: int = 0
    # 缓存与缓冲区占用字节数
    cached: int = 0
    # 可用内存字节数
    available: int = 0
    # 当前 MoviePilot 进程使用内存占总内存百分比
    usage: float = 0.0


class ScheduleProgress(BaseModel):
    """后台服务执行进度信息。"""

    # ID
    id: str | None = None
    # 名称
    name: str | None = None
    # 多语言名称
    name_i18n: str | None = None
    # 提供者
    provider: str | None = None
    # 多语言提供者
    provider_i18n: str | None = None
    # 是否正在执行
    enable: bool | None = False
    # 当前完成百分比
    value: float | None = 0.0
    # 当前进度文本
    text: str | None = None
    # 多语言进度文本
    text_i18n: str | None = None
    # 执行状态 waiting/running/success/failed
    status: str | None = None
    # 最近一次执行是否成功
    success: bool | None = None
    # 最近一次开始时间
    started_at: str | None = None
    # 最近一次结束时间
    finished_at: str | None = None
    # 最近一次错误信息
    error: str | None = None
    # 多语言错误信息
    error_i18n: str | None = None
    # 扩展数据
    data: dict | None = Field(default_factory=dict)

    @model_validator(mode="after")
    def fill_i18n_fields(self) -> ScheduleProgress:
        """
        自动补充后台服务进度的多语言展示字段。
        """
        locale = LocaleHelper.get_current_locale()
        if self.name and self.name_i18n is None:
            self.name_i18n = LocaleHelper.translate_text(self.name, locale=locale)
        if self.provider and self.provider_i18n is None:
            self.provider_i18n = LocaleHelper.translate_text(self.provider, locale=locale)
        if self.text and self.text_i18n is None:
            self.text_i18n = LocaleHelper.translate_text(self.text, locale=locale)
        if self.error and self.error_i18n is None:
            self.error_i18n = LocaleHelper.translate_text(self.error, locale=locale)
        return self


class ScheduleInfo(BaseModel):
    """仪表板后台服务信息。"""

    # ID
    id: str | None = None
    # 名称
    name: str | None = None
    # 多语言名称
    name_i18n: str | None = None
    # 提供者
    provider: str | None = None
    # 多语言提供者
    provider_i18n: str | None = None
    # 状态
    status: str | None = None
    # 多语言状态
    status_i18n: str | None = None
    # 下次执行时间
    next_run: str | None = None
    # 多语言下次执行时间
    next_run_i18n: str | None = None
    # 当前完成百分比
    progress: float | None = 0.0
    # 进度文本
    progress_text: str | None = None
    # 多语言进度文本
    progress_text_i18n: str | None = None
    # 是否正在更新进度
    progress_enable: bool | None = False
    # 进度详情
    progress_detail: ScheduleProgress | None = None

    @model_validator(mode="after")
    def fill_i18n_fields(self) -> ScheduleInfo:
        """
        自动补充后台服务列表的多语言展示字段。
        """
        locale = LocaleHelper.get_current_locale()
        if self.name and self.name_i18n is None:
            self.name_i18n = LocaleHelper.translate_text(self.name, locale=locale)
        if self.provider and self.provider_i18n is None:
            self.provider_i18n = LocaleHelper.translate_text(self.provider, locale=locale)
        if self.status and self.status_i18n is None:
            self.status_i18n = LocaleHelper.translate_text(self.status, locale=locale)
        if self.next_run and self.next_run_i18n is None:
            self.next_run_i18n = LocaleHelper.translate_text(self.next_run, locale=locale)
        if self.progress_text and self.progress_text_i18n is None:
            self.progress_text_i18n = LocaleHelper.translate_text(self.progress_text, locale=locale)
        return self


class DashboardSystemInfo(BaseModel):
    """仪表板系统摘要信息。"""

    # 主机名称
    hostname: str
    # 操作系统名称
    operating_system: str
    # MoviePilot 运行时间，单位秒
    runtime: int
    # MoviePilot 后端版本
    version: str
