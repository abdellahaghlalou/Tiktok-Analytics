from pydoc import describe
from pydantic import BaseModel
from typing import List,Type,Optional


class VideoTarget(BaseModel):
    username : str
    desc : Optional[str] = None
    img : Optional[str] = None
    tags_hashtags : Optional[List[str]] = None
    videoCountWatch : Optional[str] = None
    commentCount : Optional[int] = None
    likeCount : Optional[int] = None
    comments :  Optional[List[dict]] = None
    videoId : str
    soundId : Optional[str] = None

