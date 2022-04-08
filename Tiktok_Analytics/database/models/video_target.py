from pydoc import describe
from pydantic import BaseModel
from typing import List,Type,Optional


class VideoTarget(BaseModel):
    scrape_operation_id : Optional[str] = None
    username : str
    desc : Optional[str] = None
    imgLink : Optional[str] = None
    videoLink : Optional[str] = None
    tags :  Optional[List[str]] = None
    hashtags : Optional[List[str]] = None
    tags_hashtags : Optional[List[str]] = None
    videoCountWatch : Optional[str] = None
    commentCount : Optional[int] = None
    likeCount : Optional[int] = None
    comments :  Optional[List[dict]] = None
    videoId : str
    soundId : Optional[str] = None

