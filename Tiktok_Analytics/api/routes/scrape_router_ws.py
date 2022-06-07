from fastapi import APIRouter, Depends, FastAPI,Request, WebSocket
from typing import List, Union
from pydantic import BaseModel
from requests import request
from Tiktok_Analytics.database.models.scrapeoperation import    ScrapeOperation
from Tiktok_Analytics.services.utils import logger
from ...models.user_target import UserTarget
from ...models.video_target import VideoTarget
from ...core.scrape import Scrape
from ...database.database import add_new_users, add_new_videos
from ...database.models.user import UserDB 
from ..users import  current_active_user


router = APIRouter()



@router.websocket('/ws/scrape')
async def scrape_(websocket : WebSocket) :
  
    # logger.info(f"Scrape request received by {user.email}")  
    # results = await scrape.scrape(option=item.option,targets=item.targets,request=request)
    
    await websocket.accept()

   
    while True:
        data = await websocket.receive_json()
        # print("data received : ",data.userId.id)
        scrape_operation = ScrapeOperation(user_id = data["userId"]["id"])
        # await websocket.send_json( {"message":"Scrape request received by {data.userId.id}"})
        await scrape_operation.save()
        option = data["selected_result"]["option"] 

        if option == '1':
            scrape = Scrape(scrape_operation=scrape_operation)
            async for result in scrape.scrape_videos(videos=data["selected_result"]["targets"],request=websocket):
                await websocket.send_json(result)
        
        elif option == '2':
            scrape = Scrape(scrape_operation=scrape_operation)
            async for result in scrape.scrape_users(users=data["selected_result"]["targets"],request=websocket):
                await websocket.send_json(result)


        # await websocket.send_text(f"Message text was: {data}")

    

