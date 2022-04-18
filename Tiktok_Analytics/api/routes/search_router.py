from fastapi import APIRouter, Response, Request, status, Depends
from typing import List, Optional, Union

from loguru import logger
from ...models.user_target import UserTarget
from ...models.video_target import VideoTarget
from ...core.search import Search
from ...database.models.user import UserDB
from ..users import  current_active_user

router = APIRouter()

@router.get("/api/search",response_model=List[Union[VideoTarget,UserTarget]])
def search(option : int,search_word : str,user: UserDB = Depends(current_active_user)) :
    
    logger.info(f"Search request received by {user.email}")
    search = Search(option,search_word,None)
    search.search()
    return search.search_result
    