from pydantic import BaseModel

class ScrapeOperation(BaseModel):
    id : str
    user_id : str
    time : str