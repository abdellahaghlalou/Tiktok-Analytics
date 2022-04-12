import uuid
from tortoise import  fields
from tortoise.models import Model

from Tiktok_Analytics.database.models.user import UserModel


class TimestampMixin():
    time = fields.DatetimeField(null = True,auto_now_add=True)


class ScrapeOperation(Model, TimestampMixin):
    id : fields.UUIDField(pk = True,default_func=uuid.uuid4)
    user : fields.ForeignKeyRelation[UserModel] = fields.ForeignKeyField(model_name = "models.UserModel")
    