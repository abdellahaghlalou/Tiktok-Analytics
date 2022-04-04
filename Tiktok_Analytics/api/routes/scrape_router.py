from fastapi import APIRouter, Response, Request, status, Depends,Query
from typing import List, Optional, Union
from ...database.models.user_target import UserTarget
from ...database.models.video_target import VideoTarget
from ...services.search import Search
from ...services.scrape import Scrape
from ...services.browser import Browser
from ...database.database import add_new_target

router = APIRouter()

@router.get("/api/scrape",response_model=List[Union[VideoTarget,UserTarget]])
async def scrape_(option :str , q: Optional[list[str]] = Query(None)) :  
    scrape = Scrape("111")
    result = scrape.scrape(option=1,videos=[],users=q)
    tt = await add_new_target(result)
    return result