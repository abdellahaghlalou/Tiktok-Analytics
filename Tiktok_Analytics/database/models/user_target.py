'''
Filename: user.py
Created Date: 
Author: 

Copyright (c) 2021 Henceforth
'''

from pydantic import BaseModel

class UserTarget(BaseModel):
    username: str
    img: str
    desc: str
