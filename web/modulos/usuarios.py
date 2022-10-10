import streamlit as st
import requests
import pandas as pd

# Variável para o armazenamento da URL da API
url = "http://localhost:5000/api/"

# Função para exibição dos dados em tela
def usuarios():
    st.subheader("usuarios")

    # Variáveis para autenticação de usuários
    email = st.text_input("E-mail:")
    senha = st.text_input("Senha:", type="password")

    # Criação do body para realizar a autenticação do usuário
    body = {
            "email": email,
            "senha": senha
        }

    # IF para validar se o botão de entrar foi precionado
    with st.expander("Visualizar", expanded=True):

        # IF para validar se os campos foram preenchidos corretamente
        if email == "" or senha == "":
            return st.info("Realize o login para visualizar!")
        
        login = requests.post(url+"login", json=body)
        token = login.json()["token"]

        # IF para validar se o usuário ou senha estão corretos
        if token == "Usuario ou senha incorretos":
            return st.error("Usuário ou senha incorretos")
        
        # Variável que processa o token retornado
        token = f"Bearer {token}"

        # Requisição para o endpoint de listar
        usuarios = requests.get(url+"usuarios", headers={'Authorization': token})
        usuarios = usuarios.json()["Usuarios"]

        # Criação de variáveis para o armazenamento do dados retornados da API
        usuarios_ids = []
        usuarios_nomes = []
        usuarios_emails = []
        admin = []

        # Loop para retorar cada linha
        for usuario in usuarios:
            usuarios_ids.append(usuario["id"])
            usuarios_nomes.append(usuario["nome"])
            usuarios_emails.append(usuario["email"])
            retorno_admin = usuario["admin"]

            # IF apenas para transformar True em Sim e False em Não para facilitar o uso
            if retorno_admin == True:
                admin.append("Sim")
            else:
                admin.append("Não")

        # Criação do dataframe responsável por exibir os dados
        dataframe = {"ID": usuarios_ids, "Nome": usuarios_nomes, "Email": usuarios_emails, "Admin": admin}
        df = pd.DataFrame(data=dataframe)
        df.set_index("ID", inplace=True)
        st.table(df)

    # Expander para criar na interface web o componente de Criação   
    with st.expander("Cadastrar"):
        # Variáveis para a exibição na interface web
        nome = st.text_input("Nome do usuario: ", key="nome_cadastrar")
        email = st.text_input("Email do usuario: ", key="email_cadastrar")
        senha = st.text_input("Senha do usuário: ", type="password", key="senha_cadastrar")
        admin = st.checkbox("Admin", key="admin_cadastrar")
        cadastrar = st.button("Cadastrar")

        # IF para cadastrar caso o botão seja precionado
        if cadastrar:
            body = {
                "nome": nome,
                "email": email,
                "senha": senha,
                "admin": admin
            }
            post = requests.post(url+"usuarios", headers={'Authorization': token}, json=body)
            post = post.json()

            if post["mensagem"] == "Falha ao cadastrar usuario! Mensagem: O email informado já existe!":
                return st.error("O email informado já existe!")
            st.success("Sucesso ao cadastrar usuario!")
                
    # Expander para criar na interface web o componente de Edição
    with st.expander("Editar"):
        # Variáveis responsáveis por realizar a criação do campo que trás os IDs já cadastrados
        ids = requests.get(url+"usuarios", headers={'Authorization': token})
        ids = ids.json()["Usuarios"]

        id_usuario = []
        # LOOP responsável por filtrar cadas ID retornado pela API
        for id in ids:
            id_usuario.append(id["id"])
        
        # Variáveis responsáveis pela criação dos elementos no front
        id = st.selectbox("Informe o número do usuario: ", (id_usuario), key="id_editar")
        nome = st.text_input("Nome do usuario: ", placeholder="Opcional", key="nome_editar")
        email = st.text_input("Email do usuario: ", placeholder="Opcional", key="email_editar")
        senha = st.text_input("Senha do usuário: ", placeholder="Opcional", type="password", key="senha_editar")
        admin = st.checkbox("Admin: ", key="admin_editar")
        editar = st.button("Editar")

        # IF para iniciar a edição
        if editar:            
            # IF para atualizar caso o nome seja preenchido
            if nome != "":
                body = {
                    "nome": nome,
                }
                put = requests.put(url+f"usuarios/{id}", headers={'Authorization': token}, json=body)
                st.success("usuario editado com sucesso!")

            # ELIF para atualizar caso o e-mail seja preenchido
            elif email != "":
                body = {
                    "email": email,
                }
                put = requests.put(url+f"usuarios/{id}", headers={'Authorization': token}, json=body)
                
                # IF para validar se o e-mail já existe no banco de dados
                if put.json()["mensagem"] == "Falha ao atualizar usuario! Mensagem: O email informado já existe!":
                    st.error("O email informado já existe!")
                else:
                    st.success("usuario editado com sucesso!")

            # ELIF para atualizar caso a senha seja preenchido
            elif senha != "":
                body = {
                    "senha": senha,
                }
                put = requests.put(url+f"usuarios/{id}", headers={'Authorization': token}, json=body)
                st.success("usuario editado com sucesso!")

            # ELIF para atualizar caso o admin seja preenchido
            elif admin == True or admin == False:
                body = {
                    "admin": admin
                }
                put = requests.put(url+f"usuarios/{id}", headers={'Authorization': token}, json=body)
                st.success("usuario editado com sucesso!")

            # Else para caso todos os campos sejam preenchidos
            else:  
                body = {
                        "nome": nome,
                        "email": email,
                        "senha": senha,
                        "admin": admin
                    }
                put = requests.put(url+f"usuarios/{id}", headers={'Authorization': token}, json=body)

                # IF para validar se o e-mail já existe no banco de dados
                if put.json()["mensagem"] == "Falha ao atualizar usuario! Mensagem: O email informado já existe!":
                    st.error("O email informado já existe!")
                else:
                    st.success("usuario editado com sucesso!")

    # Expander para criar na interface web o componente de Remoção
    with st.expander("Remover"):
        # Variáveis responsáveis por realizar a criação do campo que trás os IDs já cadastrados
        ids = requests.get(url+"usuarios", headers={'Authorization': token})
        ids = ids.json()["Usuarios"]

        id_usuario = []
        # LOOP responsável por filtrar cadas ID retornado pela API
        for id in ids:
            id_usuario.append(id["id"])
        
        # Variáveis responsáveis pela criação dos elementos no front
        id = st.selectbox("Informe o número do usuario: ", (id_usuario), key="id_deletar")
        deletar = st.button("Deletar")

        if deletar:
            delete = requests.delete(url+f"usuarios/{id}", headers={'Authorization': token}, json=body)
            st.success("usuario deletado com sucesso!")
