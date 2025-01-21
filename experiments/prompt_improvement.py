import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
        )
    )
)

from tqdm import tqdm
from backend.agents.prompts import analyze_comments_prompt, comment_analysis_parser
from backend.agents.connect import model
from backend.youtube.api import get_comments
import openai
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import pandas as pd


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


def build_chain(prompt, model, parser):
    analyze_comments_chain = prompt | model | parser
    return analyze_comments_chain


def rate_output(output, comments):
    rater = Rater()
    rating = rater.rating_chain.invoke(input={"comments": comments, "response": output})
    return rating


class Prompt(BaseModel):
    prompt: str = Field(description="Improved Prompt")


class PromptImprover:

    def __init__(self):
        self.improve_prompt_parser = JsonOutputParser(pydantic_object=Prompt)
        self.prompt_template = PromptTemplate(
            template="""The following prompt is used to analyze comments on a YouTube video:
                    {prompt}
                    The Rating for the current prompt is: {rating}
                    The task is to analyze the comments and provide a detailed analysis of the key points, strengths, weaknesses, and suggestions.
                    The current prompt may be improved to elicit more detailed responses from the model. Please provide a revised prompt that encourages the model to generate more insightful and informative responses.
                    The revised prompt should be more specific and detailed, guiding the model to focus on key aspects of the comments and provide a comprehensive analysis.
                    The revised prompt must be general enough to apply to a wide range of videos and comments, but specific enough to guide the model in generating relevant and informative responses.
                    Format your response like this: {format_instructions}
                    """,
            input_variables=["prompt", "rating"],
            partial_variables={
                "format_instructions": self.improve_prompt_parser.get_format_instructions()
            },
        )
        self.improve_prompt_chain = (
            self.prompt_template | model | self.improve_prompt_parser
        )

    def improve_prompt(self, prompt, rating):
        improved_prompt = self.improve_prompt_chain.invoke(
            input={"prompt": prompt, "rating": rating}
        )
        return improved_prompt["prompt"]


prompt_improver = PromptImprover()


class FullPrompt:
    def __init__(self):
        self.prompt = "Analyze the comments for a video."
        self.footer = "\n{format_instructions}\n{input}\n"
        self.full_prompt = self.prompt + self.footer
        self.analyze_comments_prompt = PromptTemplate(
            template=f"""{self.full_prompt}""",
            input_variables=["input"],
            partial_variables={
                "format_instructions": comment_analysis_parser.get_format_instructions()
            },
        )

    def build_prompt(self):
        self.full_prompt = self.prompt + self.footer
        self.analyze_comments_prompt = PromptTemplate(
            template=f"""{self.full_prompt}""",
            input_variables=["input"],
            partial_variables={
                "format_instructions": comment_analysis_parser.get_format_instructions()
            },
        )


full_prompt = FullPrompt()


def iterative_prompt_improve(video_id: str, iterations: int = 5):
    data = pd.DataFrame()
    comments = get_comments(video_id)
    prompt_improver = PromptImprover()
    data = pd.DataFrame()
    prompt = full_prompt
    analyze_comments_chain = build_chain(
        prompt.analyze_comments_prompt, model, comment_analysis_parser
    )
    data["rating"] = 0
    data["rating_reason"] = ""
    data["prompt"] = prompt.prompt
    for _ in tqdm(range(iterations), desc="Improving Prompt"):
        max_tries = 3
        while max_tries:
            try:
                output = analyze_comments_chain.invoke({"input": comments})
                rating = rate_output(output, comments)
                row = pd.DataFrame(
                    [
                        {
                            "rating": rating["rating"],
                            "rating_reason": rating["reason"],
                            "prompt": prompt.prompt,
                        }
                    ]
                )
                data = pd.concat([data, row], ignore_index=True)
                prompt.prompt = prompt_improver.improve_prompt(prompt.prompt, rating)
                prompt.build_prompt()
                print(
                    f"Tries left: {max_tries} \nRating: {rating['rating']} \nPrompt: {prompt.prompt}\n\n"
                )
                break
            except Exception as e:
                print(f"Error: {e}")
            except (openai.error.OpenAIError, ValueError) as e:
                print(f"Error: {e}")
                max_tries -= 1


if __name__ == "__main__":
    from argparse import ArgumentParser

    arg_parser = ArgumentParser()
    arg_parser.add_argument("--video_id", type=str, required=True)
    arg_parser.add_argument("--iterations", type=int, default=5)
    args = arg_parser.parse_args()
    iterative_prompt_improve(args.video_id, args.iterations)
