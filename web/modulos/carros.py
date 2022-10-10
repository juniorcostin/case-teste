import streamlit as st
import requests
import pandas as pd

# Variável para o armazenamento da URL da API
url = "http://api:5000/api/"

# Função para exibição dos dados em tela
def carros():
    st.subheader("Carros")

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
        carros = requests.get(url+"carros", headers={'Authorization': token})
        carros = carros.json()["Carros"]

        # Criação de variáveis para o armazenamento do dados retornados da API
        carros_ids = []
        carros_modelos = []
        carros_cores = []
        proprietarios = []

        # Loop para retorar cada linha
        for carro in carros:
            carros_ids.append(carro["id"])
            carros_modelos.append(carro["modelo"])
            carros_cores.append(carro["cor"])
            proprietarios.append(carro["id_proprietario"])

        # Criação do dataframe responsável por exibir os dados
        dataframe = {"ID": carros_ids, "Modelo": carros_modelos, "Cor": carros_cores, "Proprietario ID": proprietarios}
        df = pd.DataFrame(data=dataframe)
        df.set_index("ID", inplace=True)
        st.table(df)

    # Expander para criar na interface web o componente de Criação   
    with st.expander("Cadastrar"):
        # Variáveis para a exibição na interface web
        modelo = st.selectbox("Modelo do carro: ", ("Hatch", "Sedan", "Convertible"), key="modelo_cadastrar")
        cor = st.selectbox("Cor do carro: ", ("Yellow", "Blue", "Gray"), key="cor_cadastrar")

        # Variáveis responsáveis por realizar a criação do campo que trás os IDs já cadastrados
        ids = requests.get(url+"proprietarios", headers={'Authorization': token})
        ids = ids.json()["Proprietarios"]

        id_carro = []
        # LOOP responsável por filtrar cadas ID retornado pela API
        for id in ids:
            id_carro.append(id["id"])
        
        # Variáveis responsáveis pela criação dos elementos no front
        id = st.selectbox("Informe o número do proprietário: ", (id_carro), key="id_cadastrar")
        cadastrar = st.button("Cadastrar")

        # IF para cadastrar caso o botão seja precionado
        if cadastrar:
            body = {
                "modelo": modelo,
                "cor": cor,
                "id_proprietario": id
            }
            post = requests.post(url+"carros", headers={'Authorization': token}, json=body)
            post = post.json()
            st.success("Sucesso ao cadastrar Carro!")
                
    # Expander para criar na interface web o componente de Edição
    with st.expander("Editar"):
        # Variáveis responsáveis por realizar a criação do campo que trás os IDs já cadastrados
        ids = requests.get(url+"carros", headers={'Authorization': token})
        ids = ids.json()["Carros"]

        id_carro = []
        # LOOP responsável por filtrar cadas ID retornado pela API
        for id in ids:
            id_carro.append(id["id"])
        
        # Variáveis responsáveis pela criação dos elementos no front
        id = st.selectbox("Informe o número do Carro: ", (id_carro), key="id_editar")
        modelo = st.selectbox("Modelo do carro: ", (" ","Hatch", "Sedan", "Convertible"), key=("modelo_editar"), index=0)
        cor = st.selectbox("Cor do carro: ", (" ","Yellow", "Blue", "Gray"), key="cor_editar", index=0)
        editar = st.button("Editar")

        # IF para iniciar a edição
        if editar:
            
            # Else para caso os dois campos sejam preenchidos
            if modelo != " " and cor != " ":  
                body = {
                        "modelo": modelo,
                        "cor": cor
                    }
                put = requests.put(url+f"carros/{id}", headers={'Authorization': token}, json=body)
                st.write(put.json())
                st.success("Carro editado com sucesso!")

            # IF para atualizar caso o modelo seja preenchido
            elif modelo != "" and cor == " ":
                body = {
                    "modelo": modelo,
                }
                put = requests.put(url+f"carros/{id}", headers={'Authorization': token}, json=body)
                st.success("Carro editado com sucesso!")

            # ELIF para atualizar caso a cor seja preenchido
            elif cor != "" and modelo == " ":
                body = {
                    "cor": cor,
                }
                put = requests.put(url+f"carros/{id}", headers={'Authorization': token}, json=body)    
                st.success("Carro editado com sucesso!")

    # Expander para criar na interface web o componente de Remoção
    with st.expander("Remover"):
        # Variáveis responsáveis por realizar a criação do campo que trás os IDs já cadastrados
        ids = requests.get(url+"carros", headers={'Authorization': token})
        ids = ids.json()["Carros"]

        id_carro = []
        # LOOP responsável por filtrar cadas ID retornado pela API
        for id in ids:
            id_carro.append(id["id"])
        
        # Variáveis responsáveis pela criação dos elementos no front
        id = st.selectbox("Informe o número do Carro: ", (id_carro), key="id_deletar")
        deletar = st.button("Deletar")

        if deletar:
            delete = requests.delete(url+f"carros/{id}", headers={'Authorization': token}, json=body)
            st.success("Carro deletado com sucesso!")
