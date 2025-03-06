import streamlit as st
from controllers.VendedorController import (
    lista_de_vendedores,
    adicionar_vendedor,
    deletar_vendedor,
    atualizar_vendedor,
)
from routes import mudar_pagina


@st.dialog("Cadastrar Vendedor")
def cadastrar_vendedor():
    with st.form(key="form_cadastrar"):
        nome_vendedor = st.text_input(
            label="Nome do vendedor", key="input_nome_vendedor"
        )

        submitted = st.form_submit_button(label="Salvar", type="primary")

        if submitted:
            if nome_vendedor == "":
                st.error("O campo 'Nome do vendedor' não pode estar vazio.")
                return

            else:
                adicionar_vendedor(nome_vendedor)
                mudar_pagina("pagina_listar_vendedores")
                st.rerun()


@st.dialog("Editar Vendedor")
def editar_vendedor(vendedor):
    with st.form("form_editar", clear_on_submit=True):
        campo_nome = st.text_input("Nome do vendedor", value=vendedor["nome"])

        submitted = st.form_submit_button(label="Salvar", type="primary")

        if submitted:
            if campo_nome == "":
                st.error("O campo 'Nome do vendedor' não pode estar vazio.")
                return

            else:
                atualizar_vendedor(vendedor["codigo"], campo_nome)
                st.rerun()


def pagina_listar_vendedores():

    if st.button(
        label="Adicionar Vendedor",
        key="btn_incluir",
        type="primary",
    ):
        cadastrar_vendedor()

    st.header("Listagem de Vendedores", divider=True)

    vendedores = lista_de_vendedores()

    if not vendedores:
        st.info("Não há vendedores cadastrados")
    else:
        col1, col2, col3 = st.columns([0.6, 0.2, 0.2])
        col1.write("NOME")
        col2.write("")
        col3.write("")
        for vendedor in vendedores:
            col1, col2, col3 = st.columns([0.6, 0.2, 0.2])
            col1.write(vendedor["nome"])
            if col2.button(
                label="Editar",
                key=f"editar_{vendedor['codigo']}",
                use_container_width=True,
            ):
                editar_vendedor(vendedor)
            if col3.button(
                label="Remover",
                key=f"remover_{vendedor['codigo']}",
                use_container_width=True,
            ):
                deletar_vendedor(vendedor["codigo"])
                st.rerun()
