"""查询订阅分享工具"""

import json
from typing import Optional

from pydantic import BaseModel, Field

from app.agent.tools.base import MoviePilotTool
from app.agent.tools.tags import ToolTag
from app.helper.server import MoviePilotServerHelper
from app.log import logger

MAX_PAGE_SIZE = 50


class QuerySubscribeSharesInput(BaseModel):
    """查询订阅分享工具的输入参数模型"""

    name: str | None = Field(None, description="Filter shares by media name (partial match, optional)")
    page: int | None = Field(1, description="Page number for pagination (default: 1)")
    count: int | None = Field(30, description="Number of items per page (default: 30, max: 50)")
    genre_id: int | None = Field(None, description="Filter by genre ID (optional)")
    min_rating: float | None = Field(None, description="Minimum rating filter (optional, e.g., 7.5)")
    max_rating: float | None = Field(None, description="Maximum rating filter (optional, e.g., 10.0)")
    sort_type: str | None = Field(None, description="Sort type (optional, e.g., 'count', 'rating')")


class QuerySubscribeSharesTool(MoviePilotTool):
    name: str = "query_subscribe_shares"
    tags: list[str] = [
        ToolTag.Read,
        ToolTag.Subscription,
    ]
    description: str = "Query shared subscriptions from other users. Shows popular subscriptions shared by the community with filtering and pagination support."
    args_schema: type[BaseModel] = QuerySubscribeSharesInput

    def get_tool_message(self, **kwargs) -> str | None:
        """根据查询参数生成友好的提示消息"""
        name = kwargs.get("name")
        page = kwargs.get("page", 1)
        min_rating = kwargs.get("min_rating")
        max_rating = kwargs.get("max_rating")

        parts = ["查询订阅分享"]

        if name:
            parts.append(f"名称: {name}")
        if min_rating:
            parts.append(f"最低评分: {min_rating}")
        if max_rating:
            parts.append(f"最高评分: {max_rating}")
        if page > 1:
            parts.append(f"第{page}页")

        return " | ".join(parts) if len(parts) > 1 else parts[0]

    async def run(
        self,
        name: str | None = None,
        page: int | None = 1,
        count: int | None = 30,
        genre_id: int | None = None,
        min_rating: float | None = None,
        max_rating: float | None = None,
        sort_type: str | None = None,
        **kwargs,
    ) -> str:
        logger.info(
            f"执行工具: {self.name}, 参数: name={name}, page={page}, count={count}, genre_id={genre_id}, "
            f"min_rating={min_rating}, max_rating={max_rating}, sort_type={sort_type}"
        )

        try:
            if page is None or page < 1:
                page = 1
            if count is None or count < 1:
                count = 30
            # 订阅分享是外部列表型结果，限制单页大小能降低工具上下文占用。
            count = min(count, MAX_PAGE_SIZE)

            shares = await MoviePilotServerHelper.async_get_subscribe_shares(
                name=name,
                page=page,
                count=count,
                genre_id=genre_id,
                min_rating=min_rating,
                max_rating=max_rating,
                sort_type=sort_type,
            )

            if not shares:
                return "未找到订阅分享数据（可能订阅分享功能未启用）"

            # 简化字段，只保留关键信息
            simplified_shares = []
            for share in shares:
                simplified = {
                    "id": share.get("id"),
                    "name": share.get("name"),
                    "year": share.get("year"),
                    "type": share.get("type"),
                    "season": share.get("season"),
                    "tmdbid": share.get("tmdbid"),
                    "doubanid": share.get("doubanid"),
                    "bangumiid": share.get("bangumiid"),
                    "anilistid": share.get("anilistid"),
                    "media_source": share.get("media_source"),
                    "media_id": share.get("media_id"),
                    "poster": share.get("poster"),
                    "vote": share.get("vote"),
                    "share_title": share.get("share_title"),
                    "share_comment": share.get("share_comment"),
                    "share_user": share.get("share_user"),
                    "fork_count": share.get("fork_count", 0),
                }
                # 截断过长的描述
                if simplified.get("description") and len(simplified["description"]) > 200:
                    simplified["description"] = simplified["description"][:200] + "..."
                simplified_shares.append(simplified)

            result_json = json.dumps(simplified_shares, ensure_ascii=False, indent=2)

            pagination_info = f"第 {page} 页，每页 {count} 条，共 {len(simplified_shares)} 条结果"

            return f"{pagination_info}\n\n{result_json}"
        except Exception as e:
            logger.error(f"查询订阅分享失败: {e}", exc_info=True)
            return f"查询订阅分享时发生错误: {str(e)}"
