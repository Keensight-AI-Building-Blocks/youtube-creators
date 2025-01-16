from pydantic import BaseModel, Field


class VideoIdea(BaseModel):
    video_idea: str = Field(
        description="Generate a video idea for a YouTube channel using the given data."
    )


class VideoIdeas(BaseModel):
    video_ideas: list[VideoIdea] = Field(
        description="Generate a list of video ideas for a YouTube channel using the given data."
    )


class CommentAnalysis(BaseModel):
    strengths: list[str] = Field(description="List of strengths found in the comments.")
    weaknesses: list[str] = Field(
        description="List of weaknesses found in the comments."
    )
    opportunities: list[str] = Field(
        description="List of opportunities found in the comments."
    )
    suggestions: list[str] = Field(
        description="List of suggestions found in the comments."
    )
    overall_sentiment: str = Field(
        description="Describe overall sentiment of the comments."
    )


class QueryRequest(BaseModel):
    query: str
    chat_history: list[str]


class QueryResponse(BaseModel):
    answer: str
