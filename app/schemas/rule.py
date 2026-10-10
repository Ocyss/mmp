from typing import Optional

from pydantic import BaseModel


class CustomRule(BaseModel):
    """
    自定义规则项
    """

    # 规则ID
    id: str | None = None
    # 名称
    name: str | None = None
    # 包含
    include: str | None = None
    # 排除
    exclude: str | None = None
    # 大小范围（MB）
    size_range: str | None = None
    # 最少做种人数
    seeders: str | None = None
    # 发布时间
    publish_time: str | None = None


class FilterRuleGroup(BaseModel):
    """
    过滤规则组
    """

    # 名称
    name: str | None = None
    # 规则串
    rule_string: str | None = None
    # 适用类媒体类型 None-全部 电影/电视剧
    media_type: str | None = None
    # 适用媒体类别 None-全部 对应二级分类
    category: str | None = None
