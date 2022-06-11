import re
from fastapi import APIRouter, Depends, FastAPI,Request

from Tiktok_Analytics.core.analytics import analyse_data
from ...database.models.user import UserDB
from ..users import  current_active_user

router = APIRouter()

@router.post("/api/analyse",)
def analyse(user: UserDB = Depends(current_active_user)):
    analytics = analyse_data(user.id)

    return analytics