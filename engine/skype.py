import threading
from skpy import SkypeEventLoop, SkypeMessageEvent, Skype
from skpy.msg import SkypeMsg
from sqlalchemy import false
from services.messages.message import Message
from services.requests.request import Request
from services.commands.command import Command

SKP_USERNAME = "dev_elsc_shammah2@outlook.com"
SKP_PASSWORD = None
SKP_DEV_ID = "live:.cid.d722fe52835b69ad"
SKP_DEV_CHAT = "19:4cebef31750f46a3a1be882c6d93badd@thread.skype"



class SkypeListener (SkypeEventLoop):

    def __init__(self):
        super(SkypeListener, self).__init__(SKP_USERNAME, SKP_PASSWORD)

    def onEvent(self, event):
        if isinstance(event, SkypeMessageEvent):
            message = SkypeUtils.normalize(event.msg)
            message.mongo.add(message)
            command_thread = threading.Thread(
                target=SkypeUtils.is_this_command, args=(message,))
            command_thread.start()

    def run(self):
        loop_thread = threading.Thread(target=self.loop)
        loop_thread.start()


class SkypeSender(Skype):

    def __init__(self):
        super().__init__(SKP_USERNAME, SKP_PASSWORD)

    def send(self, chat : str, message : str):
        try:
            chat = self.chats.chat(chat)
            sent = chat.sendMsg(message)
            if sent:
                return True
            else:
                return false
        except Exception as e:
            print(e)
            return False

    # Necessário alterar configuração do banco MongoDB para funcionar como replicaset 
    def request(self, chat_id, content_message, listen=True, timeout=300):
        completed = [False]
        def watch_for_changes(self, mongo, request_id):
            with mongo.collection.watch() as stream:
                for change in stream:
                    if change['documentKey']['_id'] == request_id and change['updateDescription']['updatedFields'].get('solved', False):
                        completed[0] = mongo.by_id(request_id)

        request_message = self.send(chat_id, content_message)
        request_id = Message.search(request_message)
        if request_id is not None:
            request = Request(request=request_id,
                response=False, resolved=False)
        else:
            return False
        request_obj = request.mongo.add(request)
        if listen:
            thread = threading.Thread(target=watch_for_changes, args=(request.mongo,request_obj.inserted_id))
            thread.start()
            thread.join(timeout=timeout)
        if completed[0]:
            return completed[0]

        
class SkypeUtils():
    """
        As classes Utils devem possuir funções para tarefas especificas dentro da 
        plataforma, como por exemplo: pesquisas, criações, alterações etc. 
        Tais funções podem ser invocadas tanto por funcionalities, services e 
        até mesmo outras partes da Engine correspondente.
        A classe Utils também é responsavel por inicializar e implementar todos os 
        'Services' da aplicação em questão.
    """
    @classmethod
    def explain(cls, skypeMsg : SkypeMsg):
        print("id: ", skypeMsg.id)
        print("type: ", skypeMsg.type)
        print("time: ", skypeMsg.time)
        print("clientId: ", skypeMsg.clientId)
        print("userId: ", skypeMsg.userId)
        print("chatId: ", skypeMsg.chatId)
        print("content: ", skypeMsg.content)

    @classmethod
    def normalize(cls, skypeMsg : SkypeMsg):
        message = Message(
            time=skypeMsg.time,
            sender_id=skypeMsg.userId,
            recipient_id=skypeMsg.clientId,
            chat_id=skypeMsg.chatId,
            str_content=skypeMsg.content,
        )
        return message

    @classmethod
    def status(cls, object):
        try:
            return object.conn.connected
        except Exception as e:
            print(e)
            return False

    @classmethod
    def is_this_command(cls, message : Message):
        if message.str_content.startswith('!'):
            command = Command.identify(message)
            if (command):
                command.run(message)
                

class SkypeEngine():

    def __init__(self):
        self.sender = SkypeSender()
        self.listener = SkypeListener()
        Command.loader()
        Request.request_resolver()
        
    def run(self):
        self.listener.run()