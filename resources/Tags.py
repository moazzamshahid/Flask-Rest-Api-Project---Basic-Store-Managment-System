from flask_smorest import abort,Blueprint
from models import TagModel,storeModel, ItemModel
from schemas import TagSchema, StoreSchema,TagItemSchema
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError 
from db import db
from flask.views import MethodView


blp=Blueprint("Tags",__name__,description="Operation on Tags")


@blp.route("/store/<int:store_id>/tag")
class TaginStore(MethodView):
    @jwt_required()
    @blp.response(200,TagSchema(many=True))
    def get(self,store_id):
        store=storeModel.query.get_or_404(store_id)

        return store.tags.all()
    @jwt_required()
    @blp.arguments(TagSchema)
    @blp.response(200,TagSchema)
    def post(self,request_data,store_id):
        if (TagModel.query.filter(TagModel.store_id==store_id,TagModel.name == request_data["name"]).first()):
            abort(400,message="Tag exists....")
        tag=TagModel(**request_data,store_id=store_id)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500,message=str(e))
        return tag

@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagToItem(MethodView):
    @jwt_required()
    @blp.response(201,TagSchema)
    def post(self,item_id,tag_id):
        item=ItemModel.query.get_or_404(item_id)
        tag=TagModel.query.get_or_404(tag_id)
        item.tags.append(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError :
            abort(500,message="an error occured while inserting tag")
        return tag
    @jwt_required()
    @blp.response(201,TagItemSchema)
    def delete(self,item_id,tag_id):
        item=ItemModel.query.get_or_404(item_id)
        tag=TagModel.query.get_or_404(tag_id)
        item.tags.remove(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError :
            abort(500,message="an error occured while inserting tag")   

        return {"message":"item removed from tag","tag":tag,"item":item}



@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @jwt_required()
    @blp.response(200,TagSchema)
    def get(self,tag_id):
        tag=TagModel.query.get_or_404(tag_id)
        return tag

    @blp.response(202,description="Deletes a tag if no item is tagged with it",example={"message":"tag deleted"})
    @blp.alt_response(404,description="Tag not found")
    @blp.alt_response(400,description="returned if tag is assigned to one or more items.In this case tag is not deleted")
    def delete(self,tag_id):
        tag=TagModel.query.get_or_404(tag_id)
        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message":"tag deleted"}
        abort(400,message="could not delete a tag, is linked with items")


