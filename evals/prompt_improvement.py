from backend.agents.prompts import analyze_comments_prompt, comment_analysis_parser
from backend.agents.connect import model
from backend.youtube.api import get_comments
import openai
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser


class Rating(BaseModel):
    rating: float = Field(description="Rating of the response from 0-10")
    reason: str = Field(description="Reason for the rating")


class Rater:

    def __init__(self):

        self.rating_parser = JsonOutputParser(pydantic_object=Rating)
        self.rating_prompt = PromptTemplate(
            template="""This output is from a YouTube comment analysis pipeline, which analyzes comments on a given video. Your task is to carefully evaluate the quality of the analysis based on the following structure provided in the response:
                    {format_instructions}

                    Response:
                    strengths (List[str]): Key strengths identified in the comments.
                    weaknesses (List[str]): Notable weaknesses highlighted in the comments.
                    opportunities (List[str]): Potential opportunities suggested by the comments.
                    suggestions (List[str]): Specific suggestions provided by the comments.
                    overall_sentiment (str): A concise description of the overall sentiment expressed in the comments.
                    Below are the comments for the analyzed video:
                    Comments:
                    {comments}

                    Analysis Response:
                    {response}

                    Your task is to carefully evaluate the analysis provided in the Response. Grade its accuracy, clarity, and completeness, ensuring that the key points are well covered and any major issues are noted.
                    """,
            input_variables=["comments", "response"],
            partial_variables={
                "format_instructions": self.rating_parser.get_format_instructions()
            },
        )

        self.rating_chain = self.rating_prompt | model | self.rating_parser


rater = Rater()


def build_chain(prompt, model, parser):
    analyze_comments_chain = prompt | model | parser
    return analyze_comments_chain


def rate_output(output, comments):
    rating = rater.rating_chain.invoke(input={"comments": comments, "response": output})
    return rating


class Prompt(BaseModel):
    prompt: str = Field(description="Improved Prompt")


class PromptImprover:

    def __init__(self):
        self.prompt_template = PromptTemplate(
            template="""The following prompt is used to analyze comments on a YouTube video:
                    {prompt}
                    The Rating for the current prompt is: {rating}
                    The task is to analyze the comments and provide a detailed analysis of the key points, strengths, weaknesses, and suggestions.
                    The current prompt may be improved to elicit more detailed responses from the model. Please provide a revised prompt that encourages the model to generate more insightful and informative responses.
                    The revised prompt should be more specific and detailed, guiding the model to focus on key aspects of the comments and provide a comprehensive analysis.
                    """,
            input_variables=["prompt", "rating"],
        )
        self.improve_prompt_parser = JsonOutputParser(Prompt)
        self.improve_prompt_chain = (
            self.prompt_template | model | self.improve_prompt_parser
        )

    def improve_prompt(self, prompt, rating):
        improved_prompt = self.improve_prompt_chain.invoke(
            input={"prompt": prompt, "rating": rating}
        )
        return improved_prompt.prompt


prompt_improver = PromptImprover()


def analyze_comments(video_id: str, iterations: int = 5):
    comments = get_comments(video_id)
    input_text = "\n".join(comments)
    prompt = analyze_comments_prompt

    for _ in range(iterations):
        analyze_comments_chain = build_chain(prompt, model, comment_analysis_parser)
        output = analyze_comments_chain.invoke({"input": input_text})
        rating = rate_output(output, comments)
        prompt = prompt_improver.improve_prompt(prompt, rating)
    return prompt


# Example usage
video_id = "example_video_id"
result = analyze_comments(video_id, iterations=5)
print(result)
