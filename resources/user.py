from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas.user_schemas import UserSchema, UserQueryOptionalSchema, SuccessMessageSchema, UserQuerySchema
from db.user_db import UserDatabase
import hashlib
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from blocklist import  BLOCK_LIST


blueprint = Blueprint('users', __name__, description="Operations on users")


def hash_generator(string):
    return hashlib.sha256(string.encode('utf-8')).hexdigest()


@blueprint.route('/login')
class UserLogin(MethodView):
    def __init__(self):
        self.db = UserDatabase()

    @blueprint.arguments(UserSchema)
    def post(self, request_data):
        username = request_data['username']
        hashed_password = hash_generator(request_data['password'])
        # check if user exists in db

        response = self.db.verify_user(username=username, hashed_password=hashed_password)

        if response['code'] == 200:
            # username and password is correct generate JWT token
            return {'ACCESS_TOKEN': create_access_token(identity=response['identity'])}
        else:
            # user does not exists raise suitable errors
            abort(response['code'], message=response['message'])


@blueprint.route('/logout')
class UserLogout(MethodView):
    def __init__(self):
        self.db = UserDatabase()

    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCK_LIST.add(jti)
        print(BLOCK_LIST)
        return {'message': "Successfully logged out"}, 200


@blueprint.route('/users')
class User(MethodView):
    def __init__(self):
        self.db = UserDatabase()

    @blueprint.arguments(UserQueryOptionalSchema, location='query')
    @blueprint.response(200, UserSchema(many=True))
    def get(self, args):
        user_id = args.get('id')
        if user_id:
            user = self.db.get_user(user_id=user_id)
            if user:
                return [user], 201
            else:
                abort(404, message='User not found!')
        else:
            users = self.db.get_users()
            return users, 201

    @blueprint.arguments(UserSchema)
    @blueprint.response(200, SuccessMessageSchema)
    def post(self, request_data):
        if self.db.add_user(
                username=request_data['username'],
                password=hash_generator(request_data['password'])
        ):
            return {"message": "User added successfully"}, 201
        else:
            abort(403, message=f"Username: {request_data['username']} already exists! try with a different username")

    @blueprint.response(200, SuccessMessageSchema)
    @blueprint.arguments(UserQuerySchema, location='query')
    def delete(self, args):
        user_id = args.get('id')
        if self.db.delete_user(user_id=user_id):
            return {"message": "User removed successfully"}, 201
        else:
            abort(400, message=f"User with id: {user_id} not found")
