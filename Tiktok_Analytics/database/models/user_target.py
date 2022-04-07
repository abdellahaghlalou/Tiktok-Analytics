'''
Filename: user.py
Created Date: 
Author: 

Copyright (c) 2021 Henceforth
'''

from pydantic import BaseModel
from typing import Optional

class UserTarget(BaseModel):
    username: str
    nickname: Optional[str] = None
    signature : Optional[str] = None
    privateAccount : Optional[bool] = None
    isUnderAge18 : Optional[bool]  = None       
    followingCount : Optional[int] = None
    followerCount : Optional[int] = None   
    videoCount : Optional[int]  = None
    heartCount : Optional[int]  = None
    diggCount : Optional[int]   = None
    img: Optional[str]  = None
    
