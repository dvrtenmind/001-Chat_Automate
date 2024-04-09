from bson import ObjectId
from pymongo import MongoClient

DB_SYS_CLIENT = "mongodb://localhost:27017/"
DB_SYS_DATABASE = "chat_automate"
    
class Mongo():
    
    def __init__(self, collection : str):
        client = MongoClient(DB_SYS_CLIENT)
        db = client[DB_SYS_DATABASE]
        self.collection = db[collection]

    def add(self, object):
        return self.collection.insert_one(object.to_dict())
    
    def by_chat_id(self, chat_id = False):
        return self.collection.find({"chat_id": chat_id} if chat_id else {}).sort('time',1)

    
    def last_by_chat_id(self, chat_id=False):
        return self.collection.find_one({'chat_id': chat_id} if chat_id else {}, sort=[('time', -1)])
    
    
    def last_by_sender(self, sender, chat_id=False):
        return self.collection.find_one({'chat_id': chat_id, 'sender_id': sender} if chat_id else {'sender_id': sender}, sort=[('time', -1)])

    
    def by_id(self, id):
        return self.collection.find_one({'_id':ObjectId(id)})

    
    def by_periodo(self, inicial,final):
        return self.collection.find({"time": {"$gte": inicial, "$lte": final}})
    
    
    def get_x(self, parameters):
        return self.collection.find(parameters).sort('time',1)