import re
from marshmallow import Schema,fields

class plainItemSchema(Schema):
    id=fields.Int(dump_only=True)
    name=fields.Str(required=True)
    price=fields.Float(required=True)

class PlainStoreSchema(Schema):
    id=fields.Int(dump_only=True)
    name=fields.Str()

class PlainTagScema(Schema):
    id=fields.Int(dump_only=True)
    name=fields.Str()

class ItemUpdateSchema(Schema):
    name=fields.Str()
    price=fields.Float()
    store_id=fields.Int(required=True)

class ItemSchema(plainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store=fields.Nested(PlainStoreSchema(), dump_only=True)
    tags=fields.List(fields.Nested(PlainTagScema()),dump_only=True)

class StoreSchema(PlainStoreSchema):
    item=fields.List(fields.Nested(plainItemSchema()),dump_only=True)
    tags=fields.List(fields.Nested(PlainTagScema()),dump_only=True)

class TagSchema(PlainTagScema):
    store_id=fields.Int(load_only=True)
    store=fields.Nested(PlainStoreSchema(),dump_only=True)
    items=fields.List(fields.Nested(plainItemSchema()),dump_only=True)

class TagItemSchema(Schema):
    message=fields.Str()
    item=fields.Nested(ItemSchema)
    tag=fields.Nested(TagSchema)

class UserSchema(Schema):
    id=fields.Int(dump_only=True)
    username=fields.Str(required=True)
    password=fields.Str(required=True,load_only=True)








