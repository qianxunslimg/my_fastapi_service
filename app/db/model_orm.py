from tortoise import fields
from tortoise.models import Model
from bson.objectid import ObjectId


class Item(Model):
    id = fields.CharField(max_length=128, pk=True)
    name = fields.CharField(max_length=255, null=True)
    description = fields.TextField(null=True)

    @classmethod
    async def create_with_id(cls):
        return cls(id=ObjectId())
