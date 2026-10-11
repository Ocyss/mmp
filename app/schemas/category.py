from typing import Optional

from pydantic import BaseModel, ConfigDict


class CategoryRule(BaseModel):
    """
    分类规则详情
    """

    # 内容类型
    genre_ids: str | None = None
    # 语种
    original_language: str | None = None
    # 国家或地区（电视剧）
    origin_country: str | None = None
    # 国家或地区（电影）
    production_countries: str | None = None
    # 发行年份
    release_year: str | None = None
    # 允许接收其他动态字段
    model_config = ConfigDict(extra="allow")


class CategoryConfig(BaseModel):
    """
    分类策略配置
    """

    # 电影分类策略
    movie: dict[str, CategoryRule | None] | None = {}
    # 电视剧分类策略
    tv: dict[str, CategoryRule | None] | None = {}
