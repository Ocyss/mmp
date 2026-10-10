from typing import TYPE_CHECKING, Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status

from app import schemas
from app.chain.recommend import RecommendChain
from app.core.event import eventmanager
from app.core.security import verify_token
from app.modules.themoviedb.tmdbv3api.exceptions import TMDbException
from app.schemas import RecommendSourceEventData
from app.schemas.types import ChainEventType

if TYPE_CHECKING:
    from collections.abc import Awaitable

router = APIRouter()


async def _require_tmdb_result(operation: Awaitable[list[Any]]) -> list[Any]:
    """保留 TMDB 成功空列表，并把上游请求异常转换为明确的网关错误。"""
    try:
        return await operation
    except TMDbException as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="TMDB请求失败",
        ) from error


@router.get(
    "/source",
    summary="获取推荐数据源",
    response_model=list[schemas.RecommendMediaSource],
)
def source(_: schemas.TokenPayload = Depends(verify_token)) -> Any:
    """
    获取推荐数据源
    """
    # 广播事件，请示额外的推荐数据源支持
    event_data = RecommendSourceEventData()
    event = eventmanager.send_event(ChainEventType.RecommendSource, event_data)
    # 使用事件返回的上下文数据
    if event and event.event_data:
        event_data: RecommendSourceEventData = event.event_data
        if event_data.extra_sources:
            return event_data.extra_sources
    return []


@router.get(
    "/bangumi_calendar",
    summary="Bangumi每日放送",
    response_model=list[schemas.MediaInfo],
)
async def bangumi_calendar(
    page: int | None = 1,
    count: int | None = 30,
    _: schemas.TokenPayload = Depends(verify_token),
) -> Any:
    """
    浏览Bangumi每日放送
    """
    return await RecommendChain().async_bangumi_calendar(page=page, count=count)


@router.get("/douban_showing", summary="豆瓣正在热映", response_model=list[schemas.MediaInfo])
async def douban_showing(
    page: int | None = 1,
    count: int | None = 30,
    _: schemas.TokenPayload = Depends(verify_token),
) -> Any:
    """
    浏览豆瓣正在热映
    """
    return await RecommendChain().async_douban_movie_showing(page=page, count=count)


@router.get("/douban_movies", summary="豆瓣电影", response_model=list[schemas.MediaInfo])
async def douban_movies(
    sort: str | None = "R",
    tags: str | None = "",
    page: int | None = 1,
    count: int | None = 30,
    _: schemas.TokenPayload = Depends(verify_token),
) -> Any:
    """
    浏览豆瓣电影信息
    """
    return await RecommendChain().async_douban_movies(sort=sort, tags=tags, page=page, count=count)


@router.get("/douban_tvs", summary="豆瓣剧集", response_model=list[schemas.MediaInfo])
async def douban_tvs(
    sort: str | None = "R",
    tags: str | None = "",
    page: int | None = 1,
    count: int | None = 30,
    _: schemas.TokenPayload = Depends(verify_token),
) -> Any:
    """
    浏览豆瓣剧集信息
    """
    return await RecommendChain().async_douban_tvs(sort=sort, tags=tags, page=page, count=count)


@router.get(
    "/douban_movie_top250",
    summary="豆瓣电影TOP250",
    response_model=list[schemas.MediaInfo],
)
async def douban_movie_top250(
    page: int | None = 1,
    count: int | None = 30,
    _: schemas.TokenPayload = Depends(verify_token),
) -> Any:
    """
    浏览豆瓣剧集信息
    """
    return await RecommendChain().async_douban_movie_top250(page=page, count=count)


@router.get(
    "/douban_tv_weekly_chinese",
    summary="豆瓣国产剧集周榜",
    response_model=list[schemas.MediaInfo],
)
async def douban_tv_weekly_chinese(
    page: int | None = 1,
    count: int | None = 30,
    _: schemas.TokenPayload = Depends(verify_token),
) -> Any:
    """
    中国每周剧集口碑榜
    """
    return await RecommendChain().async_douban_tv_weekly_chinese(page=page, count=count)


@router.get(
    "/douban_tv_weekly_global",
    summary="豆瓣全球剧集周榜",
    response_model=list[schemas.MediaInfo],
)
async def douban_tv_weekly_global(
    page: int | None = 1,
    count: int | None = 30,
    _: schemas.TokenPayload = Depends(verify_token),
) -> Any:
    """
    全球每周剧集口碑榜
    """
    return await RecommendChain().async_douban_tv_weekly_global(page=page, count=count)


@router.get(
    "/douban_tv_animation",
    summary="豆瓣动画剧集",
    response_model=list[schemas.MediaInfo],
)
async def douban_tv_animation(
    page: int | None = 1,
    count: int | None = 30,
    _: schemas.TokenPayload = Depends(verify_token),
) -> Any:
    """
    热门动画剧集
    """
    return await RecommendChain().async_douban_tv_animation(page=page, count=count)


@router.get("/douban_movie_hot", summary="豆瓣热门电影", response_model=list[schemas.MediaInfo])
async def douban_movie_hot(
    page: int | None = 1,
    count: int | None = 30,
    _: schemas.TokenPayload = Depends(verify_token),
) -> Any:
    """
    热门电影
    """
    return await RecommendChain().async_douban_movie_hot(page=page, count=count)


@router.get("/douban_tv_hot", summary="豆瓣热门电视剧", response_model=list[schemas.MediaInfo])
async def douban_tv_hot(
    page: int | None = 1,
    count: int | None = 30,
    _: schemas.TokenPayload = Depends(verify_token),
) -> Any:
    """
    热门电视剧
    """
    return await RecommendChain().async_douban_tv_hot(page=page, count=count)


@router.get("/tmdb_movies", summary="TMDB电影", response_model=list[schemas.MediaInfo])
async def tmdb_movies(
    sort_by: str | None = "popularity.desc",
    with_genres: str | None = "",
    with_original_language: str | None = "",
    with_keywords: str | None = "",
    with_watch_providers: str | None = "",
    vote_average: float | None = 0.0,
    vote_count: int | None = 0,
    release_date: str | None = "",
    page: int | None = 1,
    _: schemas.TokenPayload = Depends(verify_token),
) -> Any:
    """
    浏览TMDB电影信息
    """
    return await _require_tmdb_result(
        RecommendChain().async_tmdb_movies(
            sort_by=sort_by,
            with_genres=with_genres,
            with_original_language=with_original_language,
            with_keywords=with_keywords,
            with_watch_providers=with_watch_providers,
            vote_average=vote_average,
            vote_count=vote_count,
            release_date=release_date,
            page=page,
            raise_exception=True,
        )
    )


@router.get("/tmdb_tvs", summary="TMDB剧集", response_model=list[schemas.MediaInfo])
async def tmdb_tvs(
    sort_by: str | None = "popularity.desc",
    with_genres: str | None = "",
    with_original_language: str | None = "",
    with_keywords: str | None = "",
    with_watch_providers: str | None = "",
    vote_average: float | None = 0.0,
    vote_count: int | None = 0,
    release_date: str | None = "",
    page: int | None = 1,
    _: schemas.TokenPayload = Depends(verify_token),
) -> Any:
    """
    浏览TMDB剧集信息
    """
    return await _require_tmdb_result(
        RecommendChain().async_tmdb_tvs(
            sort_by=sort_by,
            with_genres=with_genres,
            with_original_language=with_original_language,
            with_keywords=with_keywords,
            with_watch_providers=with_watch_providers,
            vote_average=vote_average,
            vote_count=vote_count,
            release_date=release_date,
            page=page,
            raise_exception=True,
        )
    )


@router.get("/tmdb_trending", summary="TMDB流行趋势", response_model=list[schemas.MediaInfo])
async def tmdb_trending(page: int | None = 1, _: schemas.TokenPayload = Depends(verify_token)) -> Any:
    """
    TMDB流行趋势
    """
    return await _require_tmdb_result(RecommendChain().async_tmdb_trending(page=page, raise_exception=True))
