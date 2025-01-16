from backend.agents.schemas import VideoIdeas, CommentAnalysis
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain import hub


video_ideas_parser = JsonOutputParser(pydantic_object=VideoIdeas)
comment_analysis_parser = JsonOutputParser(pydantic_object=CommentAnalysis)

video_ideas_prompt = PromptTemplate(
    template="Analyze the trending videos.\n{format_instructions}\n{input}\n",
    input_variables=["input"],
    partial_variables={
        "format_instructions": video_ideas_parser.get_format_instructions()
    },
)

analyze_comments_prompt = PromptTemplate(
    template="Analyze the comments for a video.\n{format_instructions}\n{input}\n",
    input_variables=["input"],
    partial_variables={
        "format_instructions": comment_analysis_parser.get_format_instructions()
    },
)

rag_prompt = hub.pull("rlm/rag-prompt")
