from fastapi import APIRouter, Depends,Query,Request
from typing import List, Optional, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import time , uuid
from Tiktok_Analytics.database.models.scrapeoperation import    ScrapeOperation
from Tiktok_Analytics.services.utils import logger
from ...database.models.user_target import UserTarget
from ...database.models.video_target import VideoTarget
from ...services.scrape import Scrape
from ...database.database import add_new_users, add_new_videos
from ...models.user import UserDB
from ..users import  current_active_user

router = APIRouter()

class Item(BaseModel):
    option : int
    targets : List[dict]

@router.post("/api/scrape",response_model=List[Union[VideoTarget,UserTarget]])
async def scrape_(request : Request,item:Item,user: UserDB = Depends(current_active_user)) :
    logger.info(f"Scrape request received by {user.email}")  
    print(f" {user.email}. try to scrape {item.targets}")
    # from str to uuid uuid.UUID(str)
    scrape_operation = ScrapeOperation(user_id=user.id,time=time.time())
    scrape = Scrape(scrape_operation=scrape_operation)
    results = await scrape.scrape(option=item.option,targets=item.targets)
    
    if item.option == 1:
        await add_new_users(request,results)
    if item.option == 2:
        await add_new_videos(request,results)

    return results