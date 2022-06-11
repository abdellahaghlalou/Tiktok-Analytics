'''
Filename:main.py
Created Date:
Author:

Copyright (c) 2021 Henceforth
'''
from fastapi import FastAPI
import uvicorn
from Tiktok_Analytics.api.routes import scrape_router_ws

from .configs.config import (
    API_PREFIX, APP_NAME, APP_VERSION, IS_DEBUG, HOST, PORT)
from .configs.event_handlers import start_app_handler, stop_app_handler
from .api.router import api_router
from fastapi.middleware.cors import CORSMiddleware

def get_app() -> FastAPI:
    """ Create a new instance of FastAPI with appropriate Configuration and behavior
    Returns:
        FastAPI: A modified Fast API instance
    """
    origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:4200/",
    "http://localhost:4200/"
    ]
    fast_app = FastAPI(title=APP_NAME, version=APP_VERSION, debug=IS_DEBUG)
    fast_app.include_router(api_router, prefix=API_PREFIX)
    # * Startup behavior
    fast_app.add_event_handler("startup", start_app_handler(fast_app))
    # * Shutdown behavior
    fast_app.add_event_handler("shutdown", stop_app_handler(fast_app))

    fast_app.add_middleware( 
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

    )


    return fast_app


def main():
    """Execute the application
    """
    # Creating Modified FastAPI instance
    app: FastAPI = get_app()
    uvicorn.run(app, log_level="info",port = PORT)
