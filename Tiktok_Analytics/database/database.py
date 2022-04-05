'''
Filename: database.py
Created Date: 
Author: 

Copyright (c) 2021 Henceforth
'''
from xml.dom.minidom import Document
from fastapi import FastAPI
from tortoise import Tortoise
from Tiktok_Analytics.database.models.user_target import UserTarget
#TODO update project name
from Tiktok_Analytics.services.utils import logger
from Tiktok_Analytics.configs.config import (TESTING, DATABASE_URL)
import motor.motor_asyncio



async def add_new_users(results):
    
    MONGO_DETAILS = "mongodb://localhost:27017"

    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

    database = client.tiktok

    users_collection = database.get_collection("user_target")

    
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
        result = await users_collection.insert_one(document)
       

async def add_new_videos(results):

    MONGO_DETAILS = "mongodb://localhost:27017"

    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

    database = client.tiktok

    videos_collection = database.get_collection("video_target")

    for result in results :

        document = {
            "username": result.username,
            "videoId": result.videoId,
            "soundId": result.soundId,
            "commentCount": result.commentCount,
            "likeCount": result.likeCount,
            "comments": result.comments,
        }
        result = await videos_collection.insert_one(document)