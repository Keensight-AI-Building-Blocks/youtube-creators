from backend.agents.connect import model
from backend.db import utils as db_utils
from backend.db.connect import SessionLocal
from datetime import datetime, timedelta
from backend.youtube.api import get_comments

from backend.agents.prompts import video_ideas_parser, video_ideas_prompt, analyze_comments_prompt, comment_analysis_parser




analyze_comments_chain = analyze_comments_prompt | model | comment_analysis_parser
video_ideas_chain = video_ideas_prompt | model | video_ideas_parser


def generate_video_ideas(
    buffer: int = 7,
    date: str = datetime.today().strftime("%Y-%m-%d"),
    category_id: int = 26,
):
    start_date = (
        datetime.strptime(date, "%Y-%m-%d") - timedelta(days=buffer)
    ).strftime("%Y-%m-%d")

    session = SessionLocal()
    offset = 0
    limit = 10
    trending = db_utils.get_trending_data_by_category_and_date(
        session,
        offset=offset,
        limit=limit,
        category_id=category_id,
        start_date=start_date,
        end_date=date,
    )
    session.close()
    input_text = "\n".join(
        [
            f"{item.channelTitle} - {item.title} ({item.description}) - {item.tags} - {item.view_count}"
            for item in trending
        ]
    )
    return video_ideas_chain.invoke({"input": input_text})

def analyze_comments(video_id: str):
    comments = get_comments(video_id)
    input_text = "\n".join(comments)
    return analyze_comments_chain.invoke({"input": input_text})

