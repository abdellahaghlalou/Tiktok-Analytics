'''
Filename: router.py
Created Date: 
Author: 

Copyright (c) 2020 Henceforth
'''
from tortoise.contrib.fastapi import register_tortoise
from ..configs.config import DATABASE_URL
from ..database.models.user import UserDB
from .users import auth_backend, current_active_user, fastapi_users
from fastapi import APIRouter,Depends
from .routes import configuration, authentication, search_router, scrape_router

api_router = APIRouter()
api_router.include_router(router=configuration.router)
api_router.include_router(router=search_router.router)
api_router.include_router(router=scrape_router.router)

api_router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
api_router.include_router(fastapi_users.get_register_router(), prefix="/auth", tags=["auth"])
api_router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
api_router.include_router(
    fastapi_users.get_verify_router(),
    prefix="/auth",
    tags=["auth"],
)
api_router.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])


@api_router.get("/authenticated-route")
async def authenticated_route(user: UserDB = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


register_tortoise(
    api_router,
    db_url=DATABASE_URL,
    modules={"models": ["Tiktok_Analytics.database.models.user","Tiktok_Analytics.database.models.scrapeoperation"]},
    generate_schemas=True,
)

