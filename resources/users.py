from flask import request
from flask_smorest import abort,Blueprint
from blocklist import BLOCKLIST
from flask.views import MethodView
from flask_jwt_extended import create_access_token,jwt_required,get_jwt,create_refresh_token,get_jwt_identity

from schemas import UserSchema
from models import UserModel
from db import db  
from sqlalchemy.exc import SQLAlchemyError ,IntegrityError
from passlib.hash import pbkdf2_sha256

blp=Blueprint("users",__name__,description="Operation on Users")
@jwt_required()
@blp.route("/register")
class register(MethodView):
    @blp.arguments(UserSchema)
    def post(self,user_data):
        if UserModel.query.filter(UserModel.username==user_data["username"]).first():
            abort(409,message="A user with that username already exists")
        new_user=UserModel(username=user_data["username"],password=pbkdf2_sha256.hash(user_data["password"]))
        db.session.add(new_user)
        db.session.commit()
        return {"message":"user created successfully....."},201

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self,user_data):
        user=UserModel.query.filter(UserModel.username==user_data["username"]).first()
        if user and pbkdf2_sha256.verify(user_data["password"],user.password):
            #access_token=user.username
            #print(access_token,type(access_token))
            access_token = create_access_token(identity=user.id,fresh=True)
            refresh_token=create_refresh_token(identity=user.id)
            return {"access_token":access_token,"refresh_token":refresh_token}
        abort(401,message="invalid user")

@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required()
    def post(self):
        current_user=get_jwt_identity()
        new_token=create_access_token(identity=current_user,fresh=False)
        return {"New Token":new_token}

@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200

        

@blp.route("/user/<int:user_id>")
class User(MethodView):
    @jwt_required()
    @blp.response(200,UserSchema)
    def get(self,user_id):
        user=UserModel.query.get_or_404(user_id)
        return user
    @jwt_required()
    def delete(self,user_id):
        user=UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return{"message":"user deleted successfully....."},200
