import uuid
from tortoise import  fields
from tortoise.models import Model

from Tiktok_Analytics.database.models.user import UserModel


class TimestampMixin():
    time = fields.DatetimeField(auto_now=True)


class ScrapeOperation(Model, TimestampMixin):
    id : fields.UUIDField(pk = True)
    user : fields.ForeignKeyRelation[UserModel] = fields.ForeignKeyField(model_name = "models.UserModel")
    