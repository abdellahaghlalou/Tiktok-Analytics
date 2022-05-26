'''
Filename: event_handlers.py
Created Date: 
Author: 

Copyright (c) 2021 Henceforth
'''
from typing import Coroutine
from fastapi import FastAPI
from Tiktok_Analytics.services.utils import logger
from motor.motor_asyncio import AsyncIOMotorClient
from playwright.async_api import Playwright, async_playwright


async def _startup_model(app: FastAPI) -> Coroutine:
    """code to execute when the server startup
    """
   
    # playwright = await  async_playwright().start()  
    # browser = await playwright.chromium.launch(headless=False)
    # app.context = await browser.new_context()
    app.mongodb_client = AsyncIOMotorClient("mongodb://localhost:27017")
    app.mongodb = app.mongodb_client["tiktok"]
    logger.info("Server Startup")


async def _shutdown_model(app: FastAPI) -> Coroutine:
    """code to execute when the server shutdown
    """
    app.mongodb_client.close()
    logger.info("Server Shutdown")


def start_app_handler(app: FastAPI) -> Coroutine:
    """Startup Routine
    """

    async def startup() -> None:
        # logger.info("Running app start handler.")
        await _startup_model(app)

    return startup


def stop_app_handler(app: FastAPI) -> Coroutine:
    """Shutdown Routine
    """

    async def shutdown() -> None:
        # logger.info("Running app shutdown handler.")
        await _shutdown_model(app)

    return shutdown
