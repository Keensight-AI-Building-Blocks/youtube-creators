from backend.db.models import TrendingData


def get_trending_data(session, offset: int = 0, limit: int = 10):
    return session.query(TrendingData).offset(offset).limit(limit).all()


def get_trending_data_single(session, video_id: str):
    return (
        session.query(TrendingData)
        .filter(TrendingData.video_id == video_id)
        .one_or_none()
    )


def get_trending_data_by_category(
    session, category_id: int, offset: int = 0, limit: int = 10
):
    return (
        session.query(TrendingData)
        .filter(TrendingData.categoryId == category_id)
        .offset(offset)
        .limit(limit)
        .all()
    )


def get_trending_data_by_category_and_date(
    session,
    category_id: int,
    start_date: str,
    end_date: str,
    offset: int = 0,
    limit: int = 10,
):
    return (
        session.query(TrendingData)
        .filter(TrendingData.categoryId == category_id)
        .filter(TrendingData.trending_date.between(start_date, end_date))
        .offset(offset)
        .limit(limit)
        .all()
    )
