'''
Filename: database.py
Created Date: 
Author: 

Copyright (c) 2021 Henceforth
'''
from fastapi import FastAPI
from tortoise import Tortoise
#TODO update project name
from Tiktok_Analytics.services.utils import logger
from Tiktok_Analytics.configs.config import (TESTING, DATABASE_URL)


