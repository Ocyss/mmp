from typing import Any, Dict, Optional, Union

from pydantic import BaseModel, ConfigDict, Field


class Site(BaseModel):
    # ID
    id: int | None = None
    # 站点名称
    name: str | None = None
    # 站点主域名Key
    domain: str | None = None
    # 站点地址
    url: str | None = None
    # 站点优先级
    pri: int | None = 0
    # RSS地址
    rss: str | None = None
    # Cookie
    cookie: str | None = None
    # User-Agent
    ua: str | None = None
    # ApiKey
    apikey: str | None = None
    # Token
    token: str | None = None
    # 是否使用代理
    proxy: int | None = 0
    # 过滤规则
    filter: str | None = None
    # 是否演染
    render: int | None = 0
    # 是否公开站点
    public: int | None = 0
    # 备注
    note: Any | None = None
    # 超时时间
    timeout: int | None = 15
    # 流控单位周期
    limit_interval: int | None = None
    # 流控次数
    limit_count: int | None = None
    # 流控间隔
    limit_seconds: int | None = None
    # 是否启用
    is_active: bool | None = True
    # 下载器
    downloader: str | None = None

    model_config = ConfigDict(from_attributes=True)


class SiteStatistic(BaseModel):
    # 站点ID
    domain: str | None = None
    # 成功次数
    success: int | None = 0
    # 失败次数
    fail: int | None = 0
    # 平均响应时间
    seconds: int | None = 0
    # 最后状态
    lst_state: int | None = 0
    # 最后修改时间
    lst_mod_date: str | None = None
    # 备注
    note: Any | None = None

    model_config = ConfigDict(from_attributes=True)


class SiteUserData(BaseModel):
    # 站点域名
    domain: str | None = None
    # 用户名
    username: str | None = None
    # 用户ID
    userid: str | int | None = None
    # 用户等级
    user_level: str | None = None
    # 加入时间
    join_at: str | None = None
    # 积分
    bonus: float | None = 0.0
    # 上传量
    upload: int | None = 0
    # 下载量
    download: int | None = 0
    # 分享率
    ratio: float | None = 0.0
    # 做种数
    seeding: int | None = 0
    # 下载数
    leeching: int | None = 0
    # 做种体积
    seeding_size: int | None = 0
    # 下载体积
    leeching_size: int | None = 0
    # 做种人数, 种子大小
    seeding_info: list | None = Field(default_factory=list)
    # 未读消息
    message_unread: int | None = 0
    # 未读消息内容
    message_unread_contents: list | None = Field(default_factory=list)
    # 错误信息
    err_msg: str | None = None
    # 更新日期
    updated_day: str | None = None
    # 更新时间
    updated_time: str | None = None


class SiteAuth(BaseModel):
    site: str | None = None
    params: dict[str, int | str] | None = Field(default_factory=dict)


class SiteCookieUpdate(BaseModel):
    """
    站点 Cookie 与 UA 更新请求。
    """

    username: str = Field(..., description="站点登录用户名")
    password: str = Field(..., description="站点登录密码")
    code: str | None = Field(None, description="二步验证码或密钥")


class SiteCategory(BaseModel):
    id: int | None = None
    cat: str | None = None
    desc: str | None = None
