from flask import Flask
from resources.item import blueprint as ItemBluePrint
from resources. user import blueprint as UserBluePrint
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from blocklist import BLOCK_LIST

app = Flask(__name__)

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Restaurent REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.24.2/"
app.config["JWT_SECRET_KEY"] = "658f6a1941236e707446b5d3b022779811a31f77fd067fdcf3f061d2046a7deb"

jwt_manager = JWTManager(app)

@jwt_manager.token_in_blocklist_loader
def check_if_token_in_blocked_list(jwt_header, jwt_payload):
    return jwt_payload['jti'] in BLOCK_LIST

@jwt_manager.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return (
        {
            "description": "User has been logged out",
            "error": "token revoked"
        },
        401
    )



api = Api(app)
api.register_blueprint(ItemBluePrint)
api.register_blueprint(UserBluePrint)

