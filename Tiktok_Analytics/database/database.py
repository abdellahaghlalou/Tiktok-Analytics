'''
Filename: database.py
Created Date: 
Author: 

Copyright (c) 2021 Henceforth
'''
from fastapi import FastAPI
from tortoise import Tortoise
from Tiktok_Analytics.database.models.user_target import UserTarget
#TODO update project name
from Tiktok_Analytics.services.utils import logger
from Tiktok_Analytics.configs.config import (TESTING, DATABASE_URL)
import motor.motor_asyncio



async def add_new_target(results):
    
    MONGO_DETAILS = "mongodb://localhost:27017"

    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

    database = client.tiktok

    student_collection = database.get_collection("user_target")

    
    for result in results:

        document = {
            "username": result.username,
            "nickname": result.nickname,
            "signature": result.signature,
            "privateAccount": result.privateAccount,
            "isUnderAge18": result.isUnderAge18,
            "followingCount": result.followingCount,
            "followerCount": result.followerCount,
            "videoCount": result.videoCount,
            "heartCount": result.heartCount,
            "diggCount": result.diggCount,
            "img": result.img,
        }
        result = await student_collection.insert_one(document)
       

