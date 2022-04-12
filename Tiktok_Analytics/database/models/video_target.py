from tortoise import  fields
from tortoise.models import Model
from Tiktok_Analytics.database.models.scrapeoperation import ScrapeOperation

class UserTarget(Model):
    id = fields.UUIDField(pk=True)
    scrap_operation_id :fields.ForeignKeyRelation[ScrapeOperation]= fields.ForeignKeyField('models.ScrapeOperation', related_name='user_targets', on_delete=fields.CASCADE)
    video_id = fields.CharField(max_length=255)

