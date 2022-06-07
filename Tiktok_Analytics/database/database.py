'''
Filename: database.py
Created Date: 
Author: 

Copyright (c) 2021 Henceforth
'''
from xml.dom.minidom import Document
from fastapi.encoders import jsonable_encoder
#TODO update project name
from Tiktok_Analytics.services.utils import logger
from Tiktok_Analytics.configs.config import (TESTING, DATABASE_URL)
from fastapi_users.db import TortoiseUserDatabase
from .models.user import UserDB, UserModel



async def get_user_db():
    yield TortoiseUserDatabase(UserDB, UserModel)


async def add_new_users(request,results):
      
    for result in results:

        document = jsonable_encoder(result)
        await request.app.mongodb["users"].insert_one(document)
       

async def add_new_videos(request,results):

    for result in results :

        document = jsonable_encoder(result)
        await request.app.mongodb["videos"].insert_one(document)