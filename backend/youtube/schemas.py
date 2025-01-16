from pydantic import BaseModel
from typing import List


class YoutubeComments(BaseModel):
    Comments: List[str]


class TrendingVideo(BaseModel):
    title: str
    channel: str
    description: str
    published_at: str
    view_count: str
    comment_count: str
    topic_categories: List[str]


class TrendingVideos(BaseModel):
    Videos: List[TrendingVideo]


class LoadDataRequest(BaseModel):
    video_id: str


class LoadDataResponse(BaseModel):
    message: str
    points_added: int
