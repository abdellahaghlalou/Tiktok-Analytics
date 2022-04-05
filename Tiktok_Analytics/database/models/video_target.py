from pydoc import describe
from pydantic import BaseModel
from typing import List,Type,Optional


class VideoTarget(BaseModel):
    username : str
    desc : Optional[str] = None
    img : Optional[str] = None
    tags_hashtags : Optional[List[str]] = None
    videoCountWatch : Optional[int] = None
    commentCount : int
    likeCount : int
    comments :  Optional[List[dict]] = None
    videoId : str
    soundId : str
    shareTime : Optional[str] = None

