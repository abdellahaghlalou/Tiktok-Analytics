from pydoc import describe
from pydantic import BaseModel
from typing import List

class VideoTarget(BaseModel):
    username : str
    desc : str
    img : str
    tags_hashtags : List[str]
    videoCountWatch : str
    videoId : str
