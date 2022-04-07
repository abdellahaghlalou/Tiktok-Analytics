from pydantic import BaseModel

class ScrapeOperation(BaseModel):
    user_id : str
    time : str