# Imports nencessários para que os Endpoints funcionem corretamente
import json

from configuracoes.configuracoes import db
from modulos.proprietarios import Proprietarios
from flask import Response

####################### DATABASE #######################

# CLASS que realiza a criação das colunas no banco de dados caso ele já não esteja incluso
# Também possui a função to_json que converte os campos do banco de dados para JSON
# Além das definições para encriptografia de senhas 
class Carros(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    modelo = db.Column(db.String(255), nullable=False)
    cor = db.Column(db.String(255), nullable=False)
    id_proprietario = db.Column(db.Integer, nullable=False)

    def __init__(self,
                 modelo,
                 cor,
                 id_proprietario
                 ):
        self.modelo = modelo
        self.cor = cor
        self.id_proprietario = id_proprietario

    def to_json(self):
        return {"id": self.id,
                "modelo": self.modelo,
                "cor": self.cor,
                "id_proprietario": self.id_proprietario
                }

# Endpoint GET que lista todos os carros cadastrados dentro do banco de dados
def carros_seleciona_todos():
    try:
        carros = Carros.query.filter_by()
        carros_json = [carro.to_json() for carro in carros]
        return gera_response(200, "Carros", carros_json, "Carros listados com sucesso!")
    except Exception as e:
        return gera_response(400, "Carros", {}, f"Falha ao listar Carros! Mensagem: {e}")

# Endpoint GET que lista apenas um carro, sendo filtrado pelo ID
# O ID deve ser informado na URL e também deve estar cadastrado no banco de dados
def carros_seleciona_um(id):
    try:
        # IF para validar se o ID informado está cadastrado no banco de dados
        if not Carros.query.filter_by(id=id).first():
            return gera_response(400, "Carros", {}, f"Falha ao listar carro! Mensagem: O carro ID:{id} não existe!")

        carro = Carros.query.filter_by(id=id).first()
        carros_json = carro.to_json()
        return gera_response(200, "Carros", carros_json, "Carro listado com sucesso!")
 
    except Exception as e:
        return gera_response(400, "Carros", {}, f"Falha ao listar carro! Mensagem: {e}")

# Endpoint POST que é responsável por realizar a criação de um novo carro dentro do banco de dados
# Deve ser informado o body da requisição com as informações corretas para a criação
def carros_criar(body, current_user):
    try:
        # Criação de variáveis para a validação se o usuário cupre os requisitos
        login_admin = current_user.admin
        body_id_proprietario = body["id_proprietario"]
        quantidade_carros = Carros.query.filter_by(id_proprietario=body_id_proprietario).count()

        # IF para validar se o proprietário informado está cadatrado no banco de dados
        if not Proprietarios.query.filter_by(id=body_id_proprietario).first():
            return gera_response(400, "Carros", {}, f"Erro ao cadastrar carro! Mensagem: O proprietário informado não existe")

        # IF para validar a quantidade de carros pertencentes ao proprietáio
        if quantidade_carros >= 3:
            return gera_response(400, "Carros", {}, f"Erro ao cadastrar carro! Mensagem: O proprietário informado atingiu o limite de carros")

        # IF que valida se o usuário tem as permissões necessárias para realizar a criação
        if login_admin == True:
            # Campo que realiza o commit dentro da tabela de carros
            carro = Carros(
                modelo=body["modelo"],
                cor=body["cor"],
                id_proprietario=body_id_proprietario
            )
            db.session.add(carro)
            db.session.commit()
            quantidade_carros = Carros.query.filter_by(id_proprietario=body_id_proprietario).count()

            # Campo para atualizar a quantidade de carros pertencentes ao proprietário
            proprietarios = Proprietarios.query.filter_by(id=body_id_proprietario).first()
            proprietarios.quantidade_carros = quantidade_carros
            db.session.add(proprietarios)
            db.session.commit()

            # IF Else para atualizar o campo de oportunidade venda caso o proprietário tenha 3 carros
            if quantidade_carros >= 3:
                proprietario = Proprietarios.query.filter_by(id=body_id_proprietario).first()
                proprietario.oportunidade_venda = False
                db.session.add(proprietario)
                db.session.commit()
            else:
                proprietario = Proprietarios.query.filter_by(id=body_id_proprietario).first()
                proprietario.oportunidade_venda = True
                db.session.add(proprietario)
                db.session.commit()

            return gera_response(201, "Carros", carro.to_json(), "carro cadastrado com sucesso!")
        else:
            return gera_response(403, "Carros", {}, "Você não tem permissão para cadastrar o carro!")
    except Exception as e:
        print(e)
        return gera_response(400, "Carros", {}, f"Erro ao Cadastrar carro:{e}")

# Endpoint PUT responsável pela atualização de carros
# Deve ser informado o ID do carro existente no banco de dados
# O body da requisição não necessáriamente precisa conter todos os campos
def carros_atualiza(id, body, current_user):
    try:
        # Criação de variáveis para a validação se o usuário cupre os requisitos
        login_admin = current_user.admin

        # IF para validar se o ID informado está cadastrado no banco de dados
        if not Carros.query.filter_by(id=id).first():
            return gera_response(400, "Carros", {}, f"Falha ao atualizar carro! Mensagem: O carro ID:{id} não existe!") 

        carros = Carros.query.filter_by(id=id).first()
        
        # IF para validar se o usuário tem as permissões nencessárias para editar
        if login_admin == True:

            # IF para iniciar as validações dos campos informados no body
            if "modelo" in body:
                carros.modelo = body["modelo"]
            if "cor" in body:
                carros.cor = body["cor"]
        
            db.session.add(carros)
            db.session.commit()
            return gera_response(200, "Carros", carros.to_json(), "Carro atualizado com sucesso!")

        else:
            return gera_response(403, "Carros", {}, "Você não tem permissão para atualizar o carro!")
        
    except Exception as e:
        return gera_response(400, "Carros", {}, f"Erro ao Atualizar carro:{e}")

# Endpoint DELETE responsável por deletar um carro
# Deve ser informado o ID do carro 
def carros_deleta(id, current_user):
    try:
        # Criação de variáveis para a validação se o usuário cupre os requisitos
        login_admin = current_user.admin

        # IF para validar se o ID informado está cadastrado no banco de dados
        if not Carros.query.filter_by(id=id).first():
            return gera_response(400, "Carros", {}, f"Falha ao deletar roprietario! Mensagem: O carro ID:{id} não existe!")

        carros = Carros.query.filter_by(id=id).first()
        carros_json = carros.to_json()

        # IF para validar se o usuário tem a permissão necessária para deletar
        if login_admin == True:
            db.session.delete(carros)
            db.session.commit()

            quantidade_carros = Carros.query.filter_by(id_proprietario=carros_json["id_proprietario"]).count()
            # Campo para atualizar a quantidade de carros pertencentes ao proprietário
            proprietarios = Proprietarios.query.filter_by(id=carros_json["id_proprietario"]).first()
            proprietarios.quantidade_carros = quantidade_carros
            db.session.add(proprietarios)
            db.session.commit()

            # IF Else para atualizar o campo de oportunidade venda caso o proprietário tenha 3 carros
            if quantidade_carros >= 3:
                proprietario = Proprietarios.query.filter_by(id=carros_json["id_proprietario"]).first()
                proprietario.oportunidade_venda = False
                db.session.add(proprietario)
                db.session.commit()
            else:
                proprietario = Proprietarios.query.filter_by(id=carros_json["id_proprietario"]).first()
                proprietario.oportunidade_venda = True
                db.session.add(proprietario)
                db.session.commit()
                
            return gera_response(200, "Carros", carros.to_json(), "Carros deletado com sucesso!")
    except Exception as e:
        return gera_response(400, "Carros", {}, f"Erro ao deletar carro! Mensagem:{e}")

##################### Função para a geração de mensagens de erro/sucesso ########################
def gera_response(status, nome_conteudo, conteudo, mensagem = False):
    body = {}
    body[nome_conteudo] = conteudo
    if(mensagem):
        body["mensagem"] = mensagem
    return Response(json.dumps(body, default=str), status= status, mimetype="application/json")
