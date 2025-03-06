import streamlit as st
from controllers.ClienteController import (
    lista_de_clientes,
    adicionar_cliente,
    deletar_cliente,
    atualizar_cliente,
)
from routes import mudar_pagina


@st.dialog("Cadastrar Cliente")
def cadastrar_cliente():
    with st.form("form_cadastrar", clear_on_submit=True):
        nome_cliente = st.text_input(label="Nome do cliente", key="input_nome_cliente")

        submitted = st.form_submit_button(label="Salvar", type="primary")

        if submitted:
            if nome_cliente == "":
                st.error("O campo 'Nome do cliente' não pode estar vazio.")
                return

            else:
                adicionar_cliente(nome_cliente)
                mudar_pagina("pagina_listar_clientes")
                st.rerun()


@st.dialog("Editar Cliente")
def editar_cliente(cliente):
    with st.form("form_editar", clear_on_submit=True):
        campo_nome = st.text_input("Nome do cliente", value=cliente["nome"])

        submitted = st.form_submit_button(label="Salvar", type="primary")

        if submitted:
            if campo_nome == "":
                st.error("O campo 'Nome do cliente' não pode estar vazio.")
                return

            else:
                atualizar_cliente(cliente["codigo"], campo_nome)
                st.rerun()


def pagina_listar_clientes():

    if st.button(
        label="Adicionar Cliente",
        key="btn_incluir",
        type="primary",
    ):
        cadastrar_cliente()

    st.header("Listagem de Clientes", divider=True)

    clientes = lista_de_clientes()

    if not clientes:
        st.info("Não há clientes cadastrados")
    else:
        col1, col2, col3 = st.columns([0.6, 0.2, 0.2])
        col1.write("NOME")
        col2.write("")
        col3.write("")
        for cliente in clientes:
            col1, col2, col3 = st.columns([0.6, 0.2, 0.2])
            col1.write(cliente["nome"])
            if col2.button(
                label="Editar",
                key=f"editar_{cliente['codigo']}",
                use_container_width=True,
            ):
                editar_cliente(cliente)
            if col3.button(
                label="Remover",
                key=f"remover_{cliente['codigo']}",
                use_container_width=True,
            ):
                deletar_cliente(cliente["codigo"])
                st.rerun()
