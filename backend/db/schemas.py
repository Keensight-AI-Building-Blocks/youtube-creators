from datetime import datetime
from pydantic import BaseModel
from typing import List


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


class HealthCheckResponse(BaseModel):
    status: str
    uptime: str
    current_time: str


class MetadataResponse(BaseModel):
    Debug: bool
    Frontend_Origins: List[str]
    API_Key_Set: bool
    Model_Name: str
    Base_URL: str
