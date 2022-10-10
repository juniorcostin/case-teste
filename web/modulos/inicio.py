import streamlit as st
import requests
import pandas as pd

def inicio():
    # Variável para o armazenamento da URL da API
    url = "http://api:5000/api/"

    body = {
        "email": "viewer@viewer.com",
        "senha": "viewer@viewer.com"
    }
    login = requests.post(url+"login", json=body)
    token = login.json()["token"]
    token = f"Bearer {token}"


    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Lista de Proprietários")
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

        with col2:
            st.subheader("Lista de Carros")
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