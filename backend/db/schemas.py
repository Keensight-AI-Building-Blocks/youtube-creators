from datetime import datetime
from pydantic import BaseModel


class TrendingDataDetailedSchema(BaseModel):
    video_id: str
    title: str
    publishedAt: datetime
    channelId: str
    channelTitle: str
    categoryId: int
    trending_date: datetime
    tags: str
    view_count: int
    likes: int
    dislikes: int
    comment_count: int
    thumbnail_link: str
    comments_disabled: bool
    ratings_disabled: bool
    description: str

    class Config:
        from_attributes = True


class TrendingDataSchema(BaseModel):
    video_id: str
    title: str
    publishedAt: datetime
    channelTitle: str
    categoryId: int
    trending_date: datetime
    tags: str
    view_count: int
    likes: int
    dislikes: int
    description: str

    class Config:
        from_attributes = True


class GenerateVideoIdeasInput(BaseModel):
    category_id: int
    date: str
    buffer: int


# class GenerateVideoIdeasOutput(BaseModel):
#     video_ideas: list[str]
