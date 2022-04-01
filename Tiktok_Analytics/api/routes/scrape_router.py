from fastapi import APIRouter, Response, Request, status, Depends,Query
from typing import List, Optional, Union
from ...database.models.user import User
from ...database.models.video import Video
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