import importlib
import pkgutil
from database.mongodb.mongo import Mongo
from engine.skype import SkypeSender

class Command():
    mongo = Mongo('commands')
    id = False
    name = "NAME"
    invoke = ""
    description = "Descrição de ação do comando"
    public = True
    commands = {}
    sender = SkypeSender()

    @classmethod
    def loader(cls):
        for loader, name, is_pkg in pkgutil.walk_packages(path=['services/commands/defined']):
            module = importlib.import_module(f'services.commands.defined.{name}')
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (
                    isinstance(attr, type)
                    and issubclass(attr, Command)
                ):
                    cls.commands[attr_name.lower()] = attr()
        if len(cls.commands) > 0:
            print(f"Comandos importados, {len(cls.commands)-1} importados")
            cls.list()
        else:
            print("Nenhum comando encontrado para importação, verifique os códigos.")

    @classmethod
    def list(cls):
        i = 0
        for command in cls.commands.values():
            if i != 0:
                print(f"{i} - {command.invoke}")
            i = i+1
        print("\n")

    @classmethod
    def get_description(cls):
        return cls.name + " - " + cls.description

    @classmethod
    def identify(cls, message):
        for _, comando in cls.commands.items():
            if message.str_content.lower() == comando.invoke:
                return comando
        return False

    def run(self, message,):
        if not self.public:
            validate = self.validate(
                sender=message.sender_id, chat=message.chat_id)
            if validate:
                action = self.action(message)
                return action
            else:
                return False
        else:
            action = self.action()
            return action

    def action(self, message):
        print("Void Command")
        
    def validate(self):
        pass
    
        