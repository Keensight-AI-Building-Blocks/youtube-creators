from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class TrendingData(Base):
    __tablename__ = "youtube_trending"
    __table_args__ = {"extend_existing": True}

    video_id = Column("video_id", String, primary_key=True)
    title = Column("title", String)
    publishedAt = Column("publishedAt", DateTime)
    channelId = Column("channelId", String)
    channelTitle = Column("channelTitle", String)
    categoryId = Column("categoryId", Integer)
    trending_date = Column("trending_date", DateTime)
    tags = Column("tags", String)
    view_count = Column("view_count", Integer)
    likes = Column("likes", Integer)
    dislikes = Column("dislikes", Integer)
    comment_count = Column("comment_count", Integer)
    thumbnail_link = Column("thumbnail_link", String)
    comments_disabled = Column("comments_disabled", Boolean)
    ratings_disabled = Column("ratings_disabled", Boolean)
    description = Column("description", String)
