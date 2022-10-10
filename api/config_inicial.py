from modulos.usuarios import Usuarios
from modulos.carros import Carros
from modulos.proprietarios import Proprietarios
from configuracoes.configuracoes import db
import time

try:
    db.create_all()
except:
    time.sleep(10)
    db.create_all()

def primeiro_usuario():
    try:
        admin = Usuarios(
                        nome="admin",
                        email="admin@admin.com",
                        senha="boladegordura",
                        admin=True
                    )
        db.session.add(admin)
        db.session.commit()

        viewer = Usuarios(
                        nome="viewer",
                        email="viewer@viewer.com",
                        senha="viewer@viewer.com",
                        admin=False
                    )
        db.session.add(admin)
        db.session.commit()
        db.session.add(viewer)
        db.session.commit()
        print("Usuario criado com sucesso!")
    except Exception as e:
        print(f'Falha ao criar usuário! Mensagem: {e}')

primeiro_usuario()