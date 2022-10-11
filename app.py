import secrets
from flask import Flask,jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from resources.store import blp as storeBlp
from resources.item import blp as ItemBlp
from resources.Tags import blp as TagBlp
from resources.users import blp as UserBlp
from blocklist import BLOCKLIST
from db import db
import models
import secrets
import os



#from server prespective
#post used to recieve data
#get used to send data back only
#blueprint is used for to make code modular.
#marshmallow is used to make validation

def create_app(db_url=None): # this function is helpful when we have to right flask test functions
    app=Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"]=True
    app.config["API_TITLE"]="STORES REST API"
    app.config["API_VERSION"]="v1"
    app.config["OPENAPI_VERSION"]= "3.0.3"
    app.config["OPENAPI_URL_PREFIX"]="/"
    app.config["OPENAPI_SWAGGER_UI_PATH"]="/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"]="https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"]=db_url or os.getenv("DATABASE_URL","sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATION"]=False # it is kept false to prevent it from slowing
    db.init_app(app)

    @app.before_first_request
    def create_table():
        db.create_all()

    api=Api(app) #connects flask_smorest to flask app 
    app.config["JWT_SECRET_KEY"]=   str( secrets.SystemRandom().getrandbits(128)) # used for signing jwts
    jwt=JWTManager(app)
    
    migrate=Migrate(app,db)

    @jwt.additional_claims_loader
    def add_claim_to_jwt(identity):
        if identity==1:
            return {"is_admin":True}
        else:
            return {"is_admin":False}
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )    

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST


    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )
        


    api.register_blueprint(storeBlp)
    api.register_blueprint(ItemBlp)
    api.register_blueprint(TagBlp)
    api.register_blueprint(UserBlp)

    return app

