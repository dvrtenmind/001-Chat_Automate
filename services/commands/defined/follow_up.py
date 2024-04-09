from services.commands.command import Command
from database.postgresql.postgre import projeto

class FollowUp(Command):
    id = "d6881d60-6c55-489b-81fd-ca4820a43d88"
    name = "Follow - Up"
    invoke = "!follow-up"
    descricao = "Permite a um colaborador realizar um report."
    public = False

    def action(self, message):
        chat_id = message.chat_id
        def get_projeto():
            request_msg, id_dict = projeto.list('nome', "ativo = true")
            projeto_id = False
            while not projeto_id:
                prolog = "Por favor me informe em qual destes projetos você este trabalhando hoje:",
                self.sender.send(chat_id,prolog)
                temporary_id = self.sender.request(chat_id, request_msg)
                if temporary_id in id_dict.keys():
                    projeto_id = id_dict[temporary_id]
                if not projeto_id:
                    self.sender.send(chat_id,"Desculpe não consegui enteder sua resposta, por favor tente de novo!") 
                    self.sender.send(chat_id,"Caso seu projeto não esteja listado ou precise de ajuda envie !sair e procure o administrador do sistema.")
            return projeto_id
        
        def get_atividade():
            atividade = False
            request_msg = "Agora me diga a atividade realizada no projeto.",
            atividade = self.sender.request(chat_id, request_msg)
            return atividade

        # projeto = get_projeto()
        # atividade = get_atividade()
        #salvar follow-up