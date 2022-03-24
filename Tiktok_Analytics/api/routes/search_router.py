from fastapi import APIRouter, Response, Request, status, Depends

router = APIRouter()

@router.get("/api/search")
def search(option : int,search_word : str) :
    return {"message": "Hello World"}
