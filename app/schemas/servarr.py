from typing import Optional

from pydantic import BaseModel, Field


class RadarrMovie(BaseModel):
    id: int | None = None
    title: str | None = None
    year: str | int | None = None
    isAvailable: bool = False
    monitored: bool = False
    tmdbId: int | None = None
    imdbId: str | None = None
    titleSlug: str | None = None
    folderName: str | None = None
    path: str | None = None
    profileId: int | None = None
    qualityProfileId: int | None = None
    added: str | None = None
    hasFile: bool = False


class SonarrSeries(BaseModel):
    id: int | None = None
    title: str | None = None
    sortTitle: str | None = None
    seasonCount: int | None = None
    status: str | None = None
    overview: str | None = None
    network: str | None = None
    airTime: str | None = None
    images: list = Field(default_factory=list)
    remotePoster: str | None = None
    seasons: list = Field(default_factory=list)
    year: str | int | None = None
    path: str | None = None
    profileId: int | None = None
    languageProfileId: int | None = None
    seasonFolder: bool = False
    monitored: bool = False
    useSceneNumbering: bool = False
    runtime: int | None = None
    tmdbId: int | None = None
    imdbId: str | None = None
    tvdbId: int | None = None
    tvRageId: int | None = None
    tvMazeId: int | None = None
    firstAired: str | None = None
    seriesType: str | None = None
    cleanTitle: str | None = None
    titleSlug: str | None = None
    certification: str | None = None
    genres: list = Field(default_factory=list)
    tags: list = Field(default_factory=list)
    added: str | None = None
    ratings: dict | None = None
    qualityProfileId: int | None = None
    statistics: dict = Field(default_factory=dict)
    isAvailable: bool | None = False
    hasFile: bool | None = False
