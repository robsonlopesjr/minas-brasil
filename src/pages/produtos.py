import streamlit as st
from controllers.ProdutoController import (
    lista_de_produtos,
    adicionar_produto,
    deletar_produto,
    atualizar_produto,
)
from routes import mudar_pagina


@st.dialog("Cadastrar Produto")
def cadastrar_produto():
    with st.form(key="form_cadastrar"):
        descricao_produto = st.text_input(
            label="Descrição do produto", key="input_descricao_produto"
        )

        preco_produto = st.number_input(
            label="Preço do produto",
            key="input_preco_produto",
            min_value=0.01,
        )

        submitted = st.form_submit_button(label="Salvar", type="primary")

        if submitted:
            if descricao_produto == "":
                st.error("O campo 'Descrição do Produto' não pode estar vazio.")
                return

            elif float(preco_produto) <= 0:
                st.error("O campo 'Preço do Produto' não pode ser zero.")
                return

            else:
                adicionar_produto(descricao_produto, preco_produto)
                mudar_pagina("pagina_listar_produtos")
                st.rerun()


@st.dialog("Editar Produto")
def editar_produto(produto):
    with st.form("form_editar", clear_on_submit=True):
        campo_descricao = st.text_input(
            "Descrição do produto", value=produto["descricao"]
        )
        campo_preco = st.number_input(
            "Preço do produto", value=float(produto["preco"]), step=0.01
        )

        submitted = st.form_submit_button(label="Salvar", type="primary")

        if submitted:
            if campo_descricao == "":
                st.error("O campo 'Descrição do Produto' não pode estar vazio.")
                return

            elif float(campo_preco) <= 0:
                st.error("O campo 'Preço do Produto' não pode ser zero.")
                return

            else:
                atualizar_produto(produto["codigo"], campo_descricao, campo_preco)
                st.rerun()


def pagina_listar_produtos():

    if st.button(
        label="Adicionar Produto",
        key="btn_incluir",
        type="primary",
    ):
        cadastrar_produto()

    st.header("Listagem de Produtos", divider=True)

    produtos = lista_de_produtos()

    if not produtos:
        st.info("Não há produtos cadastrados")
    else:
        col1, col2, col3, col4, col5 = st.columns([0.1, 0.3, 0.2, 0.2, 0.2])
        col1.write("CÓDIGO")
        col2.write("DESCRIÇÃO")
        col3.write("PREÇO")
        col4.write("")
        col5.write("")
        for produto in produtos:
            col1, col2, col3, col4, col5 = st.columns([0.1, 0.3, 0.2, 0.2, 0.2])
            col1.write(produto["codigo"])
            col2.write(produto["descricao"])
            col3.write(f"R${produto["preco"]}")
            if col4.button(
                label="Editar",
                key=f"editar_{produto['codigo']}",
                use_container_width=True,
            ):
                editar_produto(produto)
            if col5.button(
                label="Remover",
                key=f"remover_{produto['codigo']}",
                use_container_width=True,
            ):
                deletar_produto(produto["codigo"])
                st.rerun()
