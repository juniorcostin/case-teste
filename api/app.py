# Imports nencessários para que os Endpoints funcionem corretamente
import json

from flask import Response, request

from autenticacao.autenticacao import jwt_required
from configuracoes.configuracoes import app
from modulos.carros import (carros_atualiza, carros_criar, carros_deleta,
                                carros_seleciona_todos, carros_seleciona_um)
from modulos.login import login_usuario
from modulos.proprietarios import (proprietarios_atualiza,
                                       proprietarios_criar,
                                       proprietarios_deleta,
                                       proprietarios_seleciona_todos,
                                       proprietarios_seleciona_um)
from modulos.usuarios import (usuarios_atualiza, usuarios_criar,
                                  usuarios_deleta, usuarios_seleciona_todos,
                                  usuarios_seleciona_um)



####################### LOGIN #######################
# Endpoint GET e POST para realizar o login que será salvo em cache
# Para realizar o login o usuário deve estar cadastrado no banco de dados
@app.route("/api/login", methods=["GET", "POST"])
def login():
    body = request.get_json()
    return login_usuario(body)

####################### USUARIOS #######################
# Endpoints responsáveis pelo gerenciamento de Usuários dentro do banco de dados

# Endpoint GET que lista todos os usuários cadastrados dentro do banco de dados
@app.route("/api/usuarios", methods=["GET"])
@jwt_required
def seleciona_usuarios(current_user):
        return usuarios_seleciona_todos(current_user)
    
# Endpoint GET que lista apenas um usuario, sendo filtrado pelo ID
# O ID deve ser informado na URL e também deve estar cadastrado no banco de dados
@app.route("/api/usuarios/<id>", methods=["GET"])
@jwt_required
def seleciona_usuario(id, current_user):
        return usuarios_seleciona_um(id, current_user)
    
# Endpoint POST que inclui um novo usuario no banco de dados
# Deve ser informado um body no formato JSON com os campos corretos para que seja incluído
@app.route("/api/usuarios", methods=["POST"])
@jwt_required
def cria_usuarios(current_user):
        body = request.get_json()
        return usuarios_criar(body, current_user)

# Endpoint PUT que atualiza um usuario, sendo filtrado pelo ID
# O ID deve ser informado na URL e também deve estar cadastrado no banco de dados
# Deve ser informado um body no formado JSON com os campos corretos porém opcionais para que seja atualizado
@app.route("/api/usuarios/<id>", methods=["PUT"])
@jwt_required
def atualiza_usuarios(id, current_user):
        body = request.get_json()
        return usuarios_atualiza(id, body, current_user)

# Endpoint DELETE que deleta um usuario, sendo filtrado pelo ID
# O ID deve ser informado na URL e também deve estar cadastrado no banco de dados
@app.route("/api/usuarios/<id>", methods=["DELETE"])
@jwt_required
def deleta_usuarios(id, current_user):
        return usuarios_deleta(id, current_user)

####################### PROPRIETÁRIOS #######################
# Endpoints responsáveis pelo gerenciamento de proprietários dentro do banco de dados

# Endpoint GET que lista todos os proprietários cadastrados dentro do banco de dados
@app.route("/api/proprietarios", methods=["GET"])
@jwt_required
def seleciona_proprietarios(current_user):
        return proprietarios_seleciona_todos()
    
# Endpoint GET que lista apenas um proprietário, sendo filtrado pelo ID
# O ID deve ser informado na URL e também deve estar cadastrado no banco de dados
@app.route("/api/proprietarios/<id>", methods=["GET"])
@jwt_required
def seleciona_proprietario(id, current_user):
        return proprietarios_seleciona_um(id)
    
# Endpoint POST que inclui um novo proprietário no banco de dados
# Deve ser informado um body no formato JSON com os campos corretos para que seja incluído
@app.route("/api/proprietarios", methods=["POST"])
@jwt_required
def cria_proprietarios(current_user):
        body = request.get_json()
        return proprietarios_criar(body, current_user)

# Endpoint PUT que atualiza um proprietário, sendo filtrado pelo ID
# O ID deve ser informado na URL e também deve estar cadastrado no banco de dados
# Deve ser informado um body no formado JSON com os campos corretos porém opcionais para que seja atualizado
@app.route("/api/proprietarios/<id>", methods=["PUT"])
@jwt_required
def atualiza_proprietarios(id, current_user):
        body = request.get_json()
        return proprietarios_atualiza(id, body, current_user)

# Endpoint DELETE que deleta um proprietário, sendo filtrado pelo ID
# O ID deve ser informado na URL e também deve estar cadastrado no banco de dados
@app.route("/api/proprietarios/<id>", methods=["DELETE"])
@jwt_required
def deleta_proprietarios(id, current_user):
        return proprietarios_deleta(id, current_user)

####################### CARROS #######################
# Endpoints responsáveis pelo gerenciamento de carros dentro do banco de dados

# Endpoint GET que lista todos os carros cadastrados dentro do banco de dados
@app.route("/api/carros", methods=["GET"])
@jwt_required
def seleciona_carros(current_user):
        return carros_seleciona_todos()
    
# Endpoint GET que lista apenas um carro, sendo filtrado pelo ID
# O ID deve ser informado na URL e também deve estar cadastrado no banco de dados
@app.route("/api/carros/<id>", methods=["GET"])
@jwt_required
def seleciona_carro(id, current_user):
        return carros_seleciona_um(id)
    
# Endpoint POST que inclui um novo carro no banco de dados
# Deve ser informado um body no formato JSON com os campos corretos para que seja incluído
@app.route("/api/carros", methods=["POST"])
@jwt_required
def cria_carros(current_user):
        body = request.get_json()
        return carros_criar(body, current_user)

# Endpoint PUT que atualiza um carro, sendo filtrado pelo ID
# O ID deve ser informado na URL e também deve estar cadastrado no banco de dados
# Deve ser informado um body no formado JSON com os campos corretos porém opcionais para que seja atualizado
@app.route("/api/carros/<id>", methods=["PUT"])
@jwt_required
def atualiza_carros(id, current_user):
        body = request.get_json()
        return carros_atualiza(id, body, current_user)

# Endpoint DELETE que deleta um carro, sendo filtrado pelo ID
# O ID deve ser informado na URL e também deve estar cadastrado no banco de dados
@app.route("/api/carros/<id>", methods=["DELETE"])
@jwt_required
def deleta_carros(id, current_user):
        return carros_deleta(id, current_user)

##################### Função para a geração de mensagens de erro/sucesso ########################
def gera_response(status, nome_conteudo, conteudo, mensagem = False):
    body = {}
    body[nome_conteudo] = conteudo
    if(mensagem):
        body["mensagem"] = mensagem
    return Response(json.dumps(body, default=str), status= status, mimetype="application/json")

#Inicializador Flask
#app.run(host="localhost",port=8000, debug=True ,threaded=True)

if __name__ == "__main__":
    app.run()