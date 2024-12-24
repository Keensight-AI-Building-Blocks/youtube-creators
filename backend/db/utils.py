from backend.db.models import TrendingData


def get_trending_data(session, offset: int = 0, limit: int = 10):
    return session.query(TrendingData).offset(offset).limit(limit).all()


def get_trending_data_single(session, video_id: str):
    return (
        session.query(TrendingData)
        .filter(TrendingData.video_id == video_id)
        .one_or_none()
    )
