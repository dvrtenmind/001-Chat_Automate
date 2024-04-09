from datetime import datetime
from database.mongodb.mongo import Mongo

class Message():
    mongo = Mongo('messages')
    
    def __init__(self, time: datetime, sender_id: str, recipient_id: str, chat_id: str, str_content: str):
        self.time = time
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.chat_id = chat_id
        self.str_content = str_content

    def to_dict(self):
            return {
                'time': self.time,
                'sender_id': self.sender_id,
                'recipient_id': self.recipient_id,
                'chat_id': self.chat_id,
                'str_content': self.str_content,
            }
    @classmethod
    def search(cls, message):
        doc = cls.mongo.collection.find_one(message.to_dict())
        if doc is not None:
            return doc['_id']
        else:
            return None
