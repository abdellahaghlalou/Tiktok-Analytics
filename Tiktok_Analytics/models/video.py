from pydoc import describe
from pydantic import BaseModel

class Video(BaseModel):
    username : str
    desc : str
    img : str
    tags_hashtags : str
    videoCountWatch : str
