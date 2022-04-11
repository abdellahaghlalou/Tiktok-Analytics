from fastapi import APIRouter, Response, Request, status, Depends
from typing import List, Optional, Union
from ...database.models.user_target import UserTarget
from ...database.models.video_target import VideoTarget
from ...services.search import Search
from ...models.user import UserDB
from ..users import  current_active_user

router = APIRouter()

@router.get("/api/search",response_model=List[Union[VideoTarget,UserTarget]])
def search(option : int,search_word : str,user: UserDB = Depends(current_active_user)) :
    
    print(f" {user.email}. try to search {search_word}")
    search = Search(option,search_word,None)
    search.search()
    return search.search_result
    