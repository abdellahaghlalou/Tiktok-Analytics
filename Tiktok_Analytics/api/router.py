'''
Filename: router.py
Created Date: 
Author: 

Copyright (c) 2020 Henceforth
'''

from fastapi import APIRouter
from .routes import configuration, authentication, search_router, scrape_router

api_router = APIRouter()
api_router.include_router(router=configuration.router)
api_router.include_router(router=search_router.router)
api_router.include_router(router=scrape_router.router)

