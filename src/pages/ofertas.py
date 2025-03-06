import streamlit as st
from controllers.OfertasController import (
    lista_de_ofertas,
    adicionar_oferta,
    deletar_oferta,
    atualizar_oferta,
)
from controllers.ProdutoController import lista_de_produtos


@st.dialog("Cadastrar Oferta")
def cadastrar_oferta(produtos_dict):
    with st.form("form_cadastrar", clear_on_submit=True):
        produto_escolhido = st.selectbox(
            "Selecione o Produto", list(produtos_dict.keys()), key="input_produto"
        )
        quantidade_levar = st.number_input(
            "Quantidade a Levar", min_value=1, key="input_qtd_levar"
        )
        quantidade_pagar = st.number_input(
            "Quantidade a Pagar", min_value=1, key="input_qtd_pagar"
        )

        submitted = st.form_submit_button(label="Salvar", type="primary")

        if submitted:
            if quantidade_levar <= quantidade_pagar:
                st.error(
                    "A quantidade a levar deve ser maior que a quantidade a pagar."
                )
                return

            adicionar_oferta(
                produtos_dict[produto_escolhido], quantidade_levar, quantidade_pagar
            )
            st.rerun()


@st.dialog("Editar Oferta")
def editar_oferta(produtos_dict, oferta):
    with st.form("form_editar", clear_on_submit=True):
        produto_escolhido = st.selectbox(
            label="Produto",
            options=list(produtos_dict.keys()),
            index=list(produtos_dict.values()).index(oferta["produto_id"]),
        )

        quantidade_levar = st.number_input(
            "Quantidade a Levar", min_value=1, value=oferta["quantidade_levar"]
        )

        quantidade_pagar = st.number_input(
            "Quantidade a Pagar", min_value=1, value=oferta["quantidade_pagar"]
        )

        submitted = st.form_submit_button(label="Salvar", type="primary")

        if submitted:
            if quantidade_levar <= quantidade_pagar:
                st.error(
                    "A quantidade a levar deve ser maior que a quantidade a pagar."
                )
                return

            atualizar_oferta(
                oferta["codigo"],
                produtos_dict[produto_escolhido],
                quantidade_levar,
                quantidade_pagar,
            )
            st.rerun()


def pagina_listar_ofertas():
    produtos = lista_de_produtos()
    produtos_dict = {produto["descricao"]: produto["codigo"] for produto in produtos}

    if st.button(
        label="Adicionar Oferta",
        key="btn_incluir",
        type="primary",
    ):
        cadastrar_oferta(produtos_dict)

    st.header("Listagem de Ofertas", divider=True)

    ofertas = lista_de_ofertas()

    if not ofertas:
        st.info("Não há ofertas cadastrados")
    else:
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.write("PRODUTO")
        col2.write("QUANT. LEVAR")
        col3.write("QUANT. PAGAR")
        col4.write("")
        col5.write("")
        for oferta in ofertas:
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.write(oferta["produto_descricao"])
            col2.write(oferta["quantidade_levar"])
            col3.write(oferta["quantidade_pagar"])

            if col4.button(
                label="Editar",
                key=f"editar_{oferta['codigo']}",
                use_container_width=True,
            ):
                editar_oferta(produtos_dict, oferta)
            if col5.button(
                label="Remover",
                key=f"remover_{oferta['codigo']}",
                use_container_width=True,
            ):
                deletar_oferta(oferta["codigo"])
                st.rerun()
