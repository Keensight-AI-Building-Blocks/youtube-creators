from pydantic import BaseModel, Field


class VideoIdea(BaseModel):
    video_idea: str = Field(
        description="Generate a video idea for a YouTube channel using the given data."
    )


class VideoIdeas(BaseModel):
    video_ideas: list[VideoIdea] = Field(
        description="Generate a list of video ideas for a YouTube channel using the given data."
    )
