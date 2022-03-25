from fastapi import APIRouter, Response, Request, status, Depends
from models.user import User
from models.video import Video
from services.search import Search
from services.browser import Browser

router = APIRouter()

@router.get("/api/search")
def search(option : int,search_word : str) :

    browser = Browser()
    search = Search(option,search_word)
    search.search(browser)
    return search.search_result
    