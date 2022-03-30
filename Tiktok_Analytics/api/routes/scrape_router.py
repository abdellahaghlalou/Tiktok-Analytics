from fastapi import APIRouter, Response, Request, status, Depends
from typing import List, Optional, Union
from ...models.user import User
from ...models.video import Video
from ...services.search import Search
from ...services.browser import Browser

router = APIRouter()

@router.get("/api/scrape")
def scrape(request: Request) :

    pass
    # scrape = Scrape()
    # scrape.scrape()
    # return "Success"