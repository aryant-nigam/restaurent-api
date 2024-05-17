from db.item_db import ItemDatabase
from uuid import uuid4

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas.item_schemas import ItemGetSchema, ItemSchema, SuccessMessageSchema, ItemQueryOptionalSchema, ItemQuerySchema
from flask_jwt_extended import jwt_required

blueprint = Blueprint("items", __name__, description="Operations on items")


@blueprint.route("/items")
class Item(MethodView):

    def __init__(self):
        self.db = ItemDatabase()
    # Reading an item / items

    @jwt_required()
    @blueprint.arguments(ItemQueryOptionalSchema, location="query")
    @blueprint.response(200, ItemGetSchema(many=True))
    def get(self, args):
        item_id = args.get('id')
        if id:
            item = self.db.get_item(item_id)
            return item if item else abort(404, message=f'item: {item_id} not found')
        else:
            items = self.db.get_item()
            return items

    # Creating an item
    @jwt_required()
    @blueprint.arguments(ItemSchema)
    @blueprint.response(200, SuccessMessageSchema)
    def post(self, request_data):
        item = {
                "id": uuid4().hex,
                "item": request_data
        }
        self.db.add_item(item)
        return {"message": "Item added successfully"}, 200

    # Updating an item
    @jwt_required()
    @blueprint.arguments(ItemQuerySchema, location="query")
    @blueprint.arguments(ItemSchema)
    @blueprint.response(200, SuccessMessageSchema)
    def put(self, request_data, args):
        item_id = args.get('id')
        if self.db.update_item(item_id=item_id, new_item=request_data):
            return {'message': f'one record affected {item_id}'}, 200
        else:
            abort(404, message=f'item: {item_id} not found')

    # deleting and item
    @jwt_required()
    @blueprint.arguments(ItemQuerySchema, location="query")
    @blueprint.response(200, SuccessMessageSchema)
    def delete(self, args):
        item_id = args.get('id')
        if self.db.delete_item(item_id=item_id):
            return {'message': f'one record affected {item_id}'}, 200
        else:
            abort(404, message=f'item: {id} not found')

