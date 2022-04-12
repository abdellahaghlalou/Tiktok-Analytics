'''
Filename: database.py
Created Date: 
Author: 

Copyright (c) 2021 Henceforth
'''
from xml.dom.minidom import Document
from fastapi.encoders import jsonable_encoder
from tortoise import Tortoise
#TODO update project name
from Tiktok_Analytics.services.utils import logger
from Tiktok_Analytics.configs.config import (TESTING, DATABASE_URL)
import motor.motor_asyncio
from fastapi_users.db import TortoiseUserDatabase
from .models.user import UserDB, UserModel



async def get_user_db():
    yield TortoiseUserDatabase(UserDB, UserModel)


async def add_new_users(request,results):
      
    for result in results:

        document = jsonable_encoder(result)
        await request.app.mongodb["user_target"].insert_one(document)
       

async def add_new_videos(request,results):

    for result in results :

        document = jsonable_encoder(result)
        await request.app.mongodb["video_target"].insert_one(document)