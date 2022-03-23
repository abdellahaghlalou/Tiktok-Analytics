'''
Filename: configuration.py
Created Date: 
Author: 

Copyright (c) 2021 Henceforth
'''
from fastapi import APIRouter, Response, Request, status, Depends
from Tiktok_Analytics.services.utils import logger
# create router instance
router = APIRouter()

