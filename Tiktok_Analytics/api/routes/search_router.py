from fastapi import APIRouter, Response, Request, status, Depends
from typing import List, Optional, Union
from ...models.user import User
from ...models.video import Video
from ...services.search import Search
from ...services.browser import Browser

router = APIRouter()

@router.get("/api/search",response_model=List[Union[Video,User]])
def search(option : int,search_word : str) :

    
    search = Search(option,search_word,None)
    search.search()
    return search.search_result
    