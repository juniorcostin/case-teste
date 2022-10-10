# Imports nencessários para que os Endpoints funcionem corretamente
import json

from configuracoes.configuracoes import db
from flask import Response
from werkzeug.security import check_password_hash, generate_password_hash

####################### DATABASE #######################

# CLASS que realiza a criação das colunas no banco de dados caso ele já não esteja incluso
# Também possui a função to_json que converte os campos do banco de dados para JSON
# Além das definições para encriptografia de senhas 
class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    senha = db.Column(db.String(255), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)

    def __init__(self,
                 nome,
                 email,
                 senha,
                 admin
                 ):
        self.nome = nome
        self.email = email
        self.senha = generate_password_hash(senha)
        self.admin = admin

    def verifica_senha(self, senha):
        return check_password_hash(self.senha, senha)

    def to_json(self):
        return {"id": self.id,
                "nome": self.nome,
                "email": self.email,
                "senha": self.senha,
                "admin": self.admin
                }

# Endpoint GET que lista todos os usuários cadastrados dentro do banco de dados
def usuarios_seleciona_todos(current_user):
    try:
        # Criação de variáveis para a validação se o usuário cupre os requisitos
        login_admin = current_user.admin

        # If para validar se o usuário tem as permissões
        if login_admin == True:
            usuarios = Usuarios.query.filter_by()
            usuarios_json = [usuario.to_json() for usuario in usuarios]
            return gera_response(200, "Usuarios", usuarios_json, "Usuarios listados com sucesso!")
        else:
            return gera_response(403, "Usuarios", {}, "Você não tem permissão para listar os usuários!")
    except Exception as e:
        return gera_response(400, "Usuarios", {}, f"Falha ao listar usuarios! Mensagem: {e}")

# Endpoint GET que lista apenas um dispositivo, sendo filtrado pelo ID
# O ID deve ser informado na URL e também deve estar cadastrado no banco de dados
def usuarios_seleciona_um(id, current_user):
    try:
        # Criação de variáveis para a validação se o usuário cupre os requisitos
        login_admin = current_user.admin

        # IF para validar se o ID informado está cadastrado no banco de dados
        if not Usuarios.query.filter_by(id=id).first():
            return gera_response(400, "Usuarios", {}, f"Falha ao listar usuario! Mensagem: O usuário ID:{id} não existe!")

        # If para validar se o usuário tem as permissões
        if login_admin == True:
            usuario = Usuarios.query.filter_by(id=id).first()
            usuarios_json = usuario.to_json()
            return gera_response(200, "Usuarios", usuarios_json, "Usuario listado com sucesso!")
        else:
            return gera_response(403, "Usuarios", {}, "Você não tem permissão para listar o usuário!")
    except Exception as e:
        return gera_response(400, "Usuarios", {}, f"Falha ao listar usuario! Mensagem: {e}")

# Endpoint POST que é responsável por realizar a criação de um novo usuário dentro do banco de dados
# Deve ser informado o body da requisição com as informações corretas para a criação
def usuarios_criar(body, current_user):
    try:
        # Criação de variáveis para a validação se o usuário cupre os requisitos
        login_admin = current_user.admin
        body_usuario_email = body["email"]

        # IF para validar se o email informado já está cadastrado no banco de dados
        if Usuarios.query.filter_by(email=body_usuario_email).first():
            return gera_response(400, "Usuarios", {}, f"Falha ao criar usuario! Mensagem: O email {body_usuario_email} já existe!")

        # IF que valida se o usuário tem as permissões necessárias para realizar a criação de outros usuários
        if login_admin == True:
            usuario = Usuarios(
                nome=body["nome"],
                email=body["email"],
                senha=body["senha"],
                admin=body["admin"],
            )
            db.session.add(usuario)
            db.session.commit()
            return gera_response(201, "Usuarios", usuario.to_json(), "Usuario cadastrado com sucesso!")
        else:
            return gera_response(403, "Usuarios", {}, "Você não tem permissão para cadastrar o usuário!")
    except Exception as e:
        print(e)
        return gera_response(400, "Usuarios", {}, f"Erro ao Cadastrar usuario:{e}")

# Endpoint PUT responsável pela atualização de usuários
# Deve ser informado o ID do usuário existente no banco de dados
# O body da requisição não necessáriamente precisa conter todos os campos
def usuarios_atualiza(id, body, current_user):
    try:
        # Criação de variáveis para a validação se o usuário cupre os requisitos
        login_admin = current_user.admin

        # IF para validar se o ID informado está cadastrado no banco de dados
        if not Usuarios.query.filter_by(id=id).first():
            return gera_response(400, "Usuarios", {}, f"Falha ao atualizar usuario! Mensagem: O usuário ID:{id} não existe!") 

        usuarios = Usuarios.query.filter_by(id=id).first()
        
        # IF para validar se o usuário tem as permissões nencessárias para editar o usuário
        if login_admin == True:

            # IF para iniciar as validações dos campos informados no body
            if "nome" in body:
                usuarios.nome = body["nome"]
            if "email" in body:
                email = body["email"]
                # IF para validar se o e-mail já existe no banco de dados
                if Usuarios.query.filter_by(email=email).first():
                    return gera_response(400, "Usuarios", {}, f"Falha ao atualizar usuario! Mensagem: O email:{email} já existe!") 
                usuarios.email = email
            if "senha" in body:
                senha = body["senha"]
                # Função para gerar um password criptografado dentro do banco de dados
                senha = generate_password_hash(senha)
                usuarios.senha = senha
            if "admin" in body:
                usuarios.admin = body["admin"]
        
            db.session.add(usuarios)
            db.session.commit()
            return gera_response(200, "Usuarios", usuarios.to_json(), "Usuario atualizado com sucesso!")

        else:
            return gera_response(403, "Usuarios", {}, "Você não tem permissão para atualizar o usuário!")
        
    except Exception as e:
        return gera_response(400, "Usuarios", {}, f"Erro ao Atualizar usuario:{e}")

# Endpoint DELETE responsável por deletar um usuário
# Deve ser informado o ID do usuário 
def usuarios_deleta(id, current_user):
    try:
        # Criação de variáveis para a validação se o usuário cupre os requisitos
        login_admin = current_user.admin

        # IF para validar se o ID informado está cadastrado no banco de dados
        if not Usuarios.query.filter_by(id=id).first():
            return gera_response(400, "Usuarios", {}, f"Falha ao deletar usuario! Mensagem: O usuário ID:{id} não existe!")

        usuarios = Usuarios.query.filter_by(id=id).first()

        # IF para validar se o usuário tem a permissão necessária para deletar o usuário
        if login_admin == True:
            db.session.delete(usuarios)
            db.session.commit()
            return gera_response(200, "Usuarios", usuarios.to_json(), "Usuario deletado com sucesso!")
    except Exception as e:
        return gera_response(400, "Usuarios", {}, f"Erro ao deletar usuario! Mensagem:{e}")

##################### Função para a geração de mensagens de erro/sucesso ########################
def gera_response(status, nome_conteudo, conteudo, mensagem = False):
    body = {}
    body[nome_conteudo] = conteudo
    if(mensagem):
        body["mensagem"] = mensagem
    return Response(json.dumps(body, default=str), status= status, mimetype="application/json")
