from db import db


#for many to many relationship
class ItemTagsModel(db.Model):
    __tablename__="Item_Tags"
    id=db.Column(db.Integer,primary_key=True)
    items_id=db.Column(db.Integer, db.ForeignKey("items.id"))
    tag_id=db.Column(db.Integer, db.ForeignKey("Tags.id"))