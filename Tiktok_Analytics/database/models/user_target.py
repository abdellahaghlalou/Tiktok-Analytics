'''
Filename: user_target.py
Created Date: 
Author: ABDELLAH AGHLALOU  

Copyright (c) 2021 Henceforth
'''

from pydantic import BaseModel
from typing import Optional

class UserTarget(BaseModel):
    scrap_operation_id : Optional[str]
    username: str
    nickname: Optional[str] = None
    nickname_followers: Optional[str] = None
    signature : Optional[str] = None
    privateAccount : Optional[bool] = None
    isUnderAge18 : Optional[bool]  = None       
    followingCount : Optional[int] = None
    followerCount : Optional[int] = None   
    videoCount : Optional[int]  = None
    heartCount : Optional[int]  = None
    diggCount : Optional[int]   = None
    img: Optional[str]  = None
    
