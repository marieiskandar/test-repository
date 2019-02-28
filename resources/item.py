import sqlite3
from flask_restful import reqparse, Resource
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type = float, required = True, help = "this field cannot be left blank")
    parser.add_argument('store_id', type = float, required = True, help = "this field cannot be left blank")

    @jwt_required()
    def get(self, name):
        try:
            item = ItemModel.find_by_name(name)
        except:
            return {'message' : 'error occured'}, 500
        if item :
            return item.json()
        return {'message' : 'item not found'}


    def post(self,name):
        if ItemModel.find_by_name(name) :
            return {'message' : "An item with name '{}' already exists".format(name)}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])
        try:
            item.save_to_db()
        except:
            return {'message' : 'error occured'}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item :
            item.delete_from_db()
        return {'message' : 'item deleted'}

    def put(self, name) :
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None :
            item = ItemModel(name, data['price'], data['store_id'])
        else :
            item.price = data['price']
            item.store_id = data['store_id']
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items' : list(map(lambda x : x.json(), ItemModel.query.all()))}
