from langchain_core.prompts import PromptTemplate
from backend.agents.connect import model
from langchain_core.output_parsers import JsonOutputParser
from backend.agents.schemas import VideoIdeas
from backend.db import utils as db_utils
from backend.db.connect import get_db, SessionLocal
from datetime import datetime, timedelta


parser = JsonOutputParser(pydantic_object=VideoIdeas)


prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{input}\n",
    input_variables=["input"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

video_ideas_chain = prompt | model | parser


def generate_ideas_chain(
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
