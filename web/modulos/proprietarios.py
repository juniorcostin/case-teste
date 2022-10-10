import streamlit as st
import requests
import pandas as pd

# Variável para o armazenamento da URL da API
url = "http://api:5000/api/"

# Função para exibição dos dados em tela
def proprietarios():
    st.subheader("Proprietários")

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
        proprietarios = requests.get(url+"proprietarios", headers={'Authorization': token})
        proprietarios = proprietarios.json()["Proprietarios"]

        # Criação de variáveis para o armazenamento do dados retornados da API
        proprietarios_ids = []
        proprietarios_nomes = []
        proprietarios_emails = []
        oportunidades = []
        proprietarios_carros = []

        # Loop para retorar cada linha
        for proprietario in proprietarios:
            proprietarios_ids.append(proprietario["id"])
            proprietarios_nomes.append(proprietario["nome"])
            proprietarios_emails.append(proprietario["email"])
            proprietarios_carros.append(proprietario["quantidade_carros"])
            retorno_oportunidades = proprietario["oportunidade_venda"]

            # IF apenas para transformar True em Sim e False em Não para facilitar o uso
            if retorno_oportunidades == True:
                oportunidades.append("Sim")
            else:
                oportunidades.append("Não")

        # Criação do dataframe responsável por exibir os dados
        dataframe = {"ID": proprietarios_ids, "Nome": proprietarios_nomes, "Email": proprietarios_emails, "Oportunidade p/ Venda": oportunidades, "Quantidade de Carros": proprietarios_carros}
        df = pd.DataFrame(data=dataframe)
        df.set_index("ID", inplace=True)
        st.table(df)

    # Expander para criar na interface web o componente de Criação   
    with st.expander("Cadastrar"):
        # Variáveis para a exibição na interface web
        nome = st.text_input("Nome do Proprietário")
        email = st.text_input("Email do Proprietário: ")
        cadastrar = st.button("Cadastrar")

        # IF para cadastrar caso o botão seja precionado
        if cadastrar:
            if email == "" or nome == "":
                return st.error("Nome e email são obrigatórios!")
            body = {
                "nome": nome,
                "email": email
            }
            post = requests.post(url+"proprietarios", headers={'Authorization': token}, json=body)
            post = post.json()

            if post["mensagem"] == "Falha ao cadastrar proprietario! Mensagem: O email informado já existe!":
                return st.error("O email informado já existe!")
            st.success("Sucesso ao cadastrar proprietário!")
                
    # Expander para criar na interface web o componente de Edição
    with st.expander("Editar"):
        # Variáveis responsáveis por realizar a criação do campo que trás os IDs já cadastrados
        ids = requests.get(url+"proprietarios", headers={'Authorization': token})
        ids = ids.json()["Proprietarios"]

        id_proprietario = []
        # LOOP responsável por filtrar cadas ID retornado pela API
        for id in ids:
            id_proprietario.append(id["id"])
        
        # Variáveis responsáveis pela criação dos elementos no front
        id = st.selectbox("Informe o número do proprietário: ", (id_proprietario), key="id_editar")
        nome = st.text_input("Nome do Proprietário: ", placeholder="Opcional", key="nome_editar")
        email = st.text_input("Email do Proprietário: ", placeholder="Opcional", key="email_editar")
        editar = st.button("Editar")

        # IF para iniciar a edição
        if editar:
            # IF que valida se pelo menos um campo foi preenchido
            if nome == "" and email == "":
                return st.warning("Pelo menos uma das opções deve ser preenchida!")
            
            # IF para atualizar caso o email seja preenchido
            if nome != "":
                try:
                    body = {
                        "nome": nome,
                    }
                    put = requests.put(url+f"proprietarios/{id}", headers={'Authorization': token}, json=body)
                    st.success("Proprietário editado com sucesso!")
                except:
                    st.error("Falha ao atualizar o proprietário! Contate a administração do sistema")

            # ELIF para atualizar caso o e-mail seja preenchido
            elif email != "":
                try:
                    body = {
                        "email": email,
                    }
                    put = requests.put(url+f"proprietarios/{id}", headers={'Authorization': token}, json=body)
                
                    # IF para validar se o e-mail já existe no banco de dados
                    if put.json()["mensagem"] == "Falha ao atualizar proprietario! Mensagem: O email informado já existe!":
                        st.error("O email informado já existe!")
                    else:
                        st.success("Proprietário editado com sucesso!")
                except:
                    st.error("Falha ao atualizar o proprietário! Contate a administração do sistema")

            # Else para caso os dois campos sejam preenchidos
            elif email != "" and nome !="":  
                body = {
                        "nome": nome,
                        "email": email
                    }
                put = requests.put(url+f"proprietarios/{id}", headers={'Authorization': token}, json=body)

                # IF para validar se o e-mail já existe no banco de dados
                if put.json()["mensagem"] == "Falha ao atualizar proprietario! Mensagem: O email informado já existe!":
                    st.error("O email informado já existe!")
                else:
                    st.success("Proprietário editado com sucesso!")

    # Expander para criar na interface web o componente de Remoção
    with st.expander("Remover"):
        # Variáveis responsáveis por realizar a criação do campo que trás os IDs já cadastrados
        ids = requests.get(url+"proprietarios", headers={'Authorization': token})
        ids = ids.json()["Proprietarios"]

        id_proprietario = []
        # LOOP responsável por filtrar cadas ID retornado pela API
        for id in ids:
            id_proprietario.append(id["id"])
        
        # Variáveis responsáveis pela criação dos elementos no front
        id = st.selectbox("Informe o número do proprietário: ", (id_proprietario), key="id_deletar")
        deletar = st.button("Deletar")

        if deletar:
            delete = requests.delete(url+f"proprietarios/{id}", headers={'Authorization': token}, json=body)
            st.success("Proprietário deletado com sucesso!")
