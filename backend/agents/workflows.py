from backend.agents.connect import model
from backend.youtube.api import get_comments, get_trending_videos
from pydantic import BaseModel
from langchain_core.documents import Document
from typing_extensions import List, TypedDict
from backend.youtube.connect import vector_store
from langgraph.graph import START, StateGraph

from backend.agents.prompts import (
    video_ideas_parser,
    video_ideas_prompt,
    analyze_comments_prompt,
    comment_analysis_parser,
    rag_prompt,
)


class RAG_State(TypedDict):
    question: str
    context: List[Document]
    answer: str


class TrendingVideo(BaseModel):
    title: str
    channel: str
    description: str
    published_at: str
    view_count: str
    comment_count: str
    topic_categories: List[str]


def retrieve(state: RAG_State):
    retrieved_docs = vector_store.similarity_search(state["question"])
    return {"context": retrieved_docs}


def generate(state: RAG_State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = rag_prompt.invoke(
        {"question": state["question"], "context": docs_content}
    )
    response = model.invoke(messages)
    return {"answer": response.content}


graph_builder = StateGraph(RAG_State).add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
rag_graph = graph_builder.compile()

analyze_comments_chain = analyze_comments_prompt | model | comment_analysis_parser
video_ideas_chain = video_ideas_prompt | model | video_ideas_parser


def generate_video_ideas(category_id: str):
    trending_videos = get_trending_videos(category_id)
    trending_videos_formated = []
    for video in trending_videos:
        trending_video = TrendingVideo(
            title=video["title"],
            channel=video["channel"],
            description=video.get("description", ""),
            published_at=video["published_at"],
            view_count=video["view_count"],
            comment_count=video["comment_count"],
            topic_categories=video.get("topic_categories", []),
        )
        trending_videos_formated.append(
            f"""
        Title: {trending_video.title}
        Channel: {trending_video.channel}
        Description: {trending_video.description}
        Published At: {trending_video.published_at}
        View Count: {trending_video.view_count}
        Comment Count: {trending_video.comment_count}
        Topic Categories: {", ".join(trending_video.topic_categories)}"""
        )
    input_text = "\n".join(trending_videos_formated)
    return video_ideas_chain.invoke({"input": input_text})


def analyze_comments(video_id: str):
    comments = get_comments(video_id)
    input_text = "\n".join(comments)
    return analyze_comments_chain.invoke({"input": input_text})


def query_transcripts(query: str, chat_history: List[str]):
    return {
        "answer": rag_graph.invoke({"question": query, "context": chat_history})[
            "answer"
        ]
    }
