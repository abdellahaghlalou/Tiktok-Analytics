'''
Filename: user_target.py
Created Date: 
Author: ABDELLAH AGHLALOU  

Copyright (c) 2021 Henceforth
'''

from tortoise import  fields
from tortoise.models import Model

from Tiktok_Analytics.database.models.scrapeoperation import ScrapeOperation

class UserTargetModel(Model):
    id = fields.UUIDField(pk=True)
    scrap_operation :fields.ForeignKeyRelation[ScrapeOperation]= fields.ForeignKeyField('models.ScrapeOperation', related_name='user_targets', on_delete=fields.CASCADE)
    username = fields.CharField(max_length=255)