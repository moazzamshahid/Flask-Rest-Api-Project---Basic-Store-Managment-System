from email import message
from flask import request
from flask_smorest import abort,Blueprint
from flask.views import MethodView
from schemas import ItemSchema,ItemUpdateSchema
from models import ItemModel
from flask_jwt_extended import jwt_required,get_jwt
from sqlalchemy.exc import SQLAlchemyError
from db import db
import uuid

blp=Blueprint("items",__name__,description="Operations on item")

@blp.route("/item/<int:item_id>")
class item(MethodView):
    @jwt_required()
    @blp.response(200,ItemSchema) # ItemSchema serializing Item object
    def get(self,item_id):
        item=ItemModel.query.get_or_404(item_id)
        return item
       # try:
        #    return items[item_id]
       # except KeyError:
        #    abort(401,message="Item not found.")
    @jwt_required()
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200,ItemSchema)
    def put(self,request_data,item_id): #put should be in small letters / case sensitive
        item= ItemModel.query.get(item_id)
        if item:
            item.name=request_data["name"]
            item.price=request_data["price"]
        else:
            item=ItemModel(id=item_id,**request_data)
        
        db.session.add(item)
        db.session.commit()
        return item
    
        
      
      
      #  try:
      #      item=items[item_id]
      #      item |=request_data
      #      return item
      #  except KeyError:
      #      abort(401,message="item not found")
    @jwt_required()
    def delete(self,item_id):
        jwt=get_jwt()
        if not jwt["is_admin"]:
            abort(401,message="Admin privilage required.")
        items=ItemModel.query.get_or_404(item_id)
        db.session.delete(items)
        db.session.commit()
        return {"message":"item are deleted"}
      
      
      
       # try:
       #     del items[item_id]
        #    return {"message":"item deleted"}
       # except KeyError:
       #     abort(401,message="Item not found.")

#------------------------------------------------------

@blp.route("/item")
class itemList(MethodView):
    @jwt_required()
    @blp.response(200,ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()
    #    return items.values()
    @blp.arguments(ItemSchema) #json will come through schema decorator and will be passed to post function
    @blp.response(200,ItemSchema)
    def post(self,request_data):
       # for item in items.values():
        #    if (item["name"]==request_data["name"]):
         #       abort(400,message="item already exists")
        #new_id=uuid.uuid4().hex #abchwidwjiwdwid not random
        
       # new_item={**request_data,"id":new_id}
       # items[new_id]=new_item
        new_item=ItemModel(**request_data)

        try: 
            db.session.add(new_item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="an Error occured while inserting item.")
        
        
        return new_item 