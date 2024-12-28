from pydantic import BaseModel
from typing import List

class YoutubeComments(BaseModel):
    Comments: List[str]