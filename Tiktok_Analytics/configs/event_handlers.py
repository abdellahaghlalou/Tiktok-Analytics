'''
Filename: event_handlers.py
Created Date: 
Author: 

Copyright (c) 2021 Henceforth
'''
from typing import Coroutine
from fastapi import FastAPI
from Tiktok_Analytics.services.utils import logger


async def _startup_model(app: FastAPI) -> Coroutine:
    """code to execute when the server startup
    """
    logger.info("Server Startup")


async def _shutdown_model(app: FastAPI) -> Coroutine:
    """code to execute when the server shutdown
    """
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
