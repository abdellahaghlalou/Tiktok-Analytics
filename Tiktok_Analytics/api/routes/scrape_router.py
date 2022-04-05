from fastapi import APIRouter, Depends,Query,Request
from typing import List, Optional, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from ...database.models.user_target import UserTarget
from ...database.models.video_target import VideoTarget
from ...services.scrape import Scrape
from ...database.database import add_new_users, add_new_videos

router = APIRouter()

class Item(BaseModel):
    option : int
    targets : List[dict]

@router.post("/api/scrape",response_model=List[Union[VideoTarget,UserTarget]])
async def scrape_(request : Request,item:Item) :  
    scrape = Scrape("111")
    results = await scrape.scrape(option=item.option,targets=item.targets)
    
    if item.option == 1:
        await add_new_users(request,results)
    if item.option == 2:
        await add_new_videos(request,results)

    return results