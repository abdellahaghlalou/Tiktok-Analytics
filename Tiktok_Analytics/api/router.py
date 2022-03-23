'''
Filename: router.py
Created Date: 
Author: 

Copyright (c) 2020 Henceforth
'''

from fastapi import APIRouter
from .routes import configuration, authentication

api_router = APIRouter()


