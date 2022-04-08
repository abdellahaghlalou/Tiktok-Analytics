'''
Filename: config.py
Created Date:
Author:

Copyright (c) 2021 Henceforth
'''
from starlette.datastructures import Secret
#TODO change with repo name
from Tiktok_Analytics.services.utils import config, to_bool

APP_VERSION = "0.0.1"
# TODO change with repos names
APP_NAME = "ASG"
API_PREFIX = ""

#**************** Server Configuration ****************#
# The API Key to be used with external ressources
API_KEY: Secret = config("API_KEY", cast=Secret,
                         default="WE_DON'T_NEED_API_KEY")
# Is the application is debugging
IS_DEBUG: bool = config("IS_DEBUG", cast=to_bool, default=False)
#**************** Project Configuration ****************#
# FA default host
HOST: str = config("HOST", cast=str, default="0.0.0.0")
# FA default PORT
PORT: int = config("PORT", cast=int, default=8080)
#**************** Project Testing ****************#
# Testing Environment
TESTING: bool = config("TESTING", cast=to_bool, default=True)
#**************** Celery ****************#
#**************** Postgres ****************#
# Database URl
POSTGRES_USER = config("POSTGRES_USER", cast=str, default='postgres')
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", cast=str, default='123')
POSTGRES_PORT = config("POSTGRES_PORT", cast=int, default=5050)
POSTGRES_DB = config('POSTGRES_DB', cast=str, default="db_book")
POSTGRES_HOST = config("POSTGRES_HOST", cast=str, default="localhost")

DATABASE_URL: str = f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
