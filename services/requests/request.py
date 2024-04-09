import threading
from bson import ObjectId
from database.mongodb.mongo import Mongo
from services.messages.message import Message
from typing import Optional

class Request():
    mongo = Mongo('requests')

    def __init__(self, request : ObjectId,resolved : bool, response: Optional[Message]):
        self.request = request
        self.response = response
        self.resolved = resolved
        
    def to_dict(self):
        pass

    @classmethod
    def request_resolver(cls):
        watch_thread = threading.Thread(target=cls.watch_messages)
        watch_thread.start()

    @classmethod
    def watch_messages(cls):
        with cls.mongo.collection.watch([{'$match': {'operationType': 'insert'}}]) as stream:
            for change in stream:
                message = change['fullDocument']
                chat_id = message['chat_id']
                open_request = cls.mongo.collection.find_one({'solved': False, 'request.chat_id': chat_id})
                if open_request is not None:
                    cls.solve_request(open_request, message)
        
    @classmethod
    def solve_request(cls, request, response):
        return cls.mongo.collection.update_one(
                {'_id': request['_id']},
                {'$set': {'response': response['_id'], 'solved': True}}
            )