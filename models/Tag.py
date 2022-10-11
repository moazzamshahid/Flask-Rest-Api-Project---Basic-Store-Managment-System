from db import db


class TagModel(db.Model):
    __tablename__="Tags"

    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(80), unique=True, nullable=False )
    store_id=db.Column(db.Integer,db.ForeignKey("stores.id"),unique=False, nullable=False )
    
    store=db.relationship("storeModel", back_populates="tags")
    items=db.relationship("ItemModel",back_populates="tags",secondary="Item_Tags") #it will get items by going through ItemTagModel