from fastapi import APIRouter, Response, Request, status, Depends,Query
from typing import List, Optional, Union
from ...database.models.user_target import UserTarget
from ...database.models.video_target import VideoTarget
from ...services.search import Search
from ...services.scrape import Scrape
from ...services.browser import Browser

router = APIRouter()

@router.get("/api/scrape")
def scrape_(option :str , q: Optional[list[str]] = Query(None)) :  
    scrape = Scrape("111")
    result = scrape.scrape(option=1,videos=[],users=q)
    print(result)
    return result