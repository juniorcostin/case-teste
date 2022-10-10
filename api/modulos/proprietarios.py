# Imports nencessários para que os Endpoints funcionem corretamente
import json
from configuracoes.configuracoes import db
from flask import Response

####################### DATABASE #######################

# CLASS que realiza a criação das colunas no banco de dados caso ele já não esteja incluso
# Também possui a função to_json que converte os campos do banco de dados para JSON
# Além das definições para encriptografia de senhas 
class Proprietarios(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    oportunidade_venda = db.Column(db.Boolean, nullable=False)
    quantidade_carros = db.Column(db.Integer, nullable=False)

    def __init__(self,
                 nome,
                 email,
                 oportunidade_venda,
                 quantidade_carros
                 ):
        self.nome = nome
        self.email = email
        self.oportunidade_venda = oportunidade_venda
        self.quantidade_carros = quantidade_carros

    def to_json(self):
        return {"id": self.id,
                "nome": self.nome,
                "email": self.email,
                "oportunidade_venda": self.oportunidade_venda,
                "quantidade_carros": self.quantidade_carros
                }

# Endpoint GET que lista todos os proprietarios cadastrados dentro do banco de dados
def proprietarios_seleciona_todos():
    try:
        proprietarios = Proprietarios.query.filter_by()
        proprietarios_json = [proprietario.to_json() for proprietario in proprietarios]
        return gera_response(200, "Proprietarios", proprietarios_json, "Proprietarios listados com sucesso!")

    except Exception as e:
        return gera_response(400, "Proprietarios", {}, f"Falha ao listar proprietários! Mensagem: {e}")

# Endpoint GET que lista apenas um proprietário, sendo filtrado pelo ID
# O ID deve ser informado na URL e também deve estar cadastrado no banco de dados
def proprietarios_seleciona_um(id):
    try:
        # IF para validar se o ID informado está cadastrado no banco de dados
        if not Proprietarios.query.filter_by(id=id).first():
            return gera_response(400, "Proprietarios", {}, f"Falha ao listar proprietario! Mensagem: O proprietario ID:{id} não existe!")

        proprietario = Proprietarios.query.filter_by(id=id).first()
        proprietarios_json = proprietario.to_json()
        return gera_response(200, "Proprietarios", proprietarios_json, "Proprietario listado com sucesso!")

    except Exception as e:
        return gera_response(400, "Proprietarios", {}, f"Falha ao listar proprietario! Mensagem: {e}")

# Endpoint POST que é responsável por realizar a criação de um novo proprietario dentro do banco de dados
# Deve ser informado o body da requisição com as informações corretas para a criação
def proprietarios_criar(body, current_user):
    try:
        # Criação de variáveis para a validação se o usuário cupre os requisitos
        login_admin = current_user.admin

        # IF para validar se o email informado já está cadastrado no sistema
        if Proprietarios.query.filter_by(email=body["email"]).first():
            return gera_response(400, "Proprietarios", {}, f"Falha ao cadastrar proprietario! Mensagem: O email informado já existe!")

        # IF que valida se o usuário tem as permissões necessárias para realizar a criação
        if login_admin == True:
            proprietario = Proprietarios(
                nome=body["nome"],
                email=body["email"],
                oportunidade_venda=True,
                quantidade_carros=0
            )
            db.session.add(proprietario)
            db.session.commit()
            return gera_response(201, "Proprietarios", proprietario.to_json(), "Proprietario cadastrado com sucesso!")
        else:
            return gera_response(403, "Proprietarios", {}, "Você não tem permissão para cadastrar o proprietario!")
    except Exception as e:
        print(e)
        return gera_response(400, "Proprietarios", {}, f"Erro ao Cadastrar proprietario:{e}")

# Endpoint PUT responsável pela atualização de proprietarios
# Deve ser informado o ID do proprietário existente no banco de dados
# O body da requisição não necessáriamente precisa conter todos os campos
def proprietarios_atualiza(id, body, current_user):
    try:
        # Criação de variáveis para a validação se o usuário cupre os requisitos
        login_admin = current_user.admin

        # IF para validar se o ID informado está cadastrado no banco de dados
        if not Proprietarios.query.filter_by(id=id).first():
            return gera_response(400, "Proprietarios", {}, f"Falha ao atualizar proprietario! Mensagem: O proprietário ID:{id} não existe!") 


        proprietarios = Proprietarios.query.filter_by(id=id).first()
        # IF para validar se o usuário tem as permissões nencessárias para editar
        if login_admin == True:

            # IF para iniciar as validações dos campos informados no body
            if "nome" in body:
                proprietarios.nome = body["nome"]
            if "email" in body:
                proprietarios.email = body["email"]

            db.session.add(proprietarios)
            db.session.commit()
            return gera_response(200, "Proprietarios", proprietarios.to_json(), "Proprietarios atualizado com sucesso!")

        else:
            return gera_response(403, "Proprietarios", {}, "Você não tem permissão para atualizar o proprietário!")
        
    except Exception as e:
        return gera_response(400, "Proprietarios", {}, f"Erro ao Atualizar proprietário:{e}")

# Endpoint DELETE responsável por deletar um proprietário
# Deve ser informado o ID do proprietário 
def proprietarios_deleta(id, current_user):
    try:
        # Criação de variáveis para a validação se o usuário cupre os requisitos
        login_admin = current_user.admin

        # IF para validar se o ID informado está cadastrado no banco de dados
        if not Proprietarios.query.filter_by(id=id).first():
            return gera_response(400, "Proprietarios", {}, f"Falha ao deletar roprietario! Mensagem: O proprietário ID:{id} não existe!")

        proprietarios = Proprietarios.query.filter_by(id=id).first()

        # IF para validar se o usuário tem a permissão necessária para deletar
        if login_admin == True:
            db.session.delete(proprietarios)
            db.session.commit()
            return gera_response(200, "Proprietarios", proprietarios.to_json(), "Proprietario deletado com sucesso!")
    except Exception as e:
        return gera_response(400, "Proprietarios", {}, f"Erro ao deletar proprietario! Mensagem:{e}")

##################### Função para a geração de mensagens de erro/sucesso ########################
def gera_response(status, nome_conteudo, conteudo, mensagem = False):
    body = {}
    body[nome_conteudo] = conteudo
    if(mensagem):
        body["mensagem"] = mensagem
    return Response(json.dumps(body, default=str), status= status, mimetype="application/json")
