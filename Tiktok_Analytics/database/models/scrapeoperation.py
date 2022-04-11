import uuid
from datetime import date
from pydantic import BaseModel

from tortoise import  fields
from tortoise.models import Model

class ScrapeOperation(Model):
    id : fields.UUIDField(pk = True,default_func=uuid.uuid4)
    user_id : fields.ForeignKeyField(model = "Tiktok_Analytics.models.user.UserDB")
    time : fields.DatetimeField(default_now=True)
    