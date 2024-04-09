from services.commands.command import Command

class Ping(Command):
    id = "dc10312b-6bf1-439f-902f-b4718c6db323"
    name = "Ping"
    invoke = "!ping"
    descricao = "Teste de resposta e tempo de resposta"

    def action(self, message):
        try:
            self.sender.send(message.chat_id, "Pong")
            return True
        except OSError as e:
            print(e)
            return False