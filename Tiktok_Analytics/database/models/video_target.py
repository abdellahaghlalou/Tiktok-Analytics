from tortoise import  fields
from tortoise.models import Model
from Tiktok_Analytics.database.models.scrapeoperation import ScrapeOperation

class VideoTargetModel(Model):
    id = fields.UUIDField(pk=True)
    scrap_operation :fields.ForeignKeyRelation[ScrapeOperation]= fields.ForeignKeyField('models.ScrapeOperation', related_name='video_targets', on_delete=fields.CASCADE)
    video_id = fields.CharField(max_length=255)

