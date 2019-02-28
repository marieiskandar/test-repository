from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store :
            return store.json(), 200
        return {'message' : 'Store was not found'}, 404

    def post(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return {'message' : "a store with name '{}' already exists".format(name)}, 400
        store = StoreModel(name)
        try :
            store.save_to_db()
        except :
            return {'message' : 'an error occured'}, 500
        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            try :
                store.delete_from_db()
            except :
                return {'message' : 'an error occured'}, 500
        return {'message' : 'Store deleted'}

class StoreList(Resource):
    def get (self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
