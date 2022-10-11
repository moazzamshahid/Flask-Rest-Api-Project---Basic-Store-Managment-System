from flask import request
from flask_smorest import abort,Blueprint
from flask_jwt_extended import jwt_required
from flask.views import MethodView
from schemas import StoreSchema
from models import storeModel
from db import db  
from sqlalchemy.exc import SQLAlchemyError ,IntegrityError
import uuid


blp=Blueprint("stores",__name__,description="Operations on store")

@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @jwt_required()
    @blp.response(200,StoreSchema)
    def get(self,store_id):
     store=storeModel.query.get_or_404(store_id)
     return store
       #   try:
     #       return stores[store_id]
     #   except KeyError:
     #       abort(401,message="store not found.")
    @jwt_required()
    def delete(self,store_id):

       # if item:
       #    item= ItemModel.query.get_or_404(item.id)
      #      db.session.delete(item)
          # db.session.commit()
        store = storeModel.query.get_or_404(store_id)
        try:
            db.session.delete(store)
            db.session.commit()
        except IntegrityError:
          return {"message":"store cannot be deleted, delete items first"}  
        return {"message":"store deleted"}
      #  try:
      #      del stores[store_id]
      #      return {"message":"store deleted"}
      #  except KeyError:
      #      abort(401,message="store not found.")
#------------------------------------------------------------------

@blp.route("/store")
class storeList(MethodView):
    @jwt_required()
    @blp.response(200,StoreSchema(many=True)) #many == True allow returning of list of stores
    def get(self):
        return storeModel.query.all()
       # return stores.values()
    @jwt_required()
    @blp.arguments(StoreSchema)   #json will come through schema decorator
    @blp.response(200,StoreSchema)
    def post(self,request_data):
         #   for store in stores.values():
          #      if (store["name"]==request_data["name"]):
           #         abort(400,message="store already exists")    
           # new_id=uuid.uuid4().hex #abchwidwjiwdwid not random
            
           # new_store={**request_data,"id":new_id}
           # stores[new_id]=new_store
            new_store= storeModel(**request_data) # when a new store model is created it does not check the integrity and other errors in the model
            try:
                db.session.add(new_store)
                db.session.commit()
            except IntegrityError:
                abort(400,message="Store already exists")
            except SQLAlchemyError:
                abort(500,message="an error occured while creating the store")
            
            return new_store 
#------------------------------------------------------------------
