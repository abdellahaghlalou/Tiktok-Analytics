from pydoc import describe
from pydantic import BaseModel
from typing import List,Type


class VideoTarget(BaseModel):
    username : str
    desc : str
    img : str
    tags_hashtags : List[str]
    videoCountWatch : int
    commentsCount : int
    comments : List[dict]
    videoId : str
    soundId : str
    shareTime : str

