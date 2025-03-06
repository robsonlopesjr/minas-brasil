import streamlit as st
from services.banco_de_dados import criar_banco_de_dados
# from services.dados_fakers import cadastrar_dados_fakes
from routes import mudar_pagina
import pages.clientes as PageListarClientes
import pages.produtos as PageListarProdutos
import pages.vendedores as PageListarVendedores
import pages.ofertas as PageListarOfertas
import pages.orcamentos as PageListarOrcamentos
import pages.orcamentos_cadastro as PageCadastrarOrcamentos
import pages.relatorios as PageRelatorios
from services.log import setup_logging

st.set_page_config(page_title="Minas Brasil", page_icon="📈", layout="wide")


def init():
    criar_banco_de_dados()

    if "pagina_atual" not in st.session_state:
        mudar_pagina("home")


def home():
    st.header("Minas Brasil", divider=True)
    st.subheader(
        """
        Esta é uma aplicação web desenvolvida com Streamlit que tem como objetivo gerenciar clientes, produtos, vendedores, ofertas e orçamentos. Para navegar entre os módulos selecione no menu ao lado.
        """
    )


def main():
    st.sidebar.title("Menu")
    st.sidebar.button(
        "Clientes",
        use_container_width=True,
        on_click=mudar_pagina,
        args=("pagina_listar_clientes",),
    )
    st.sidebar.button(
        "Produtos",
        use_container_width=True,
        on_click=mudar_pagina,
        args=("pagina_listar_produtos",),
    )

    st.sidebar.button(
        "Vendedores",
        use_container_width=True,
        on_click=mudar_pagina,
        args=("pagina_listar_vendedores",),
    )

    st.sidebar.button(
        "Ofertas",
        use_container_width=True,
        on_click=mudar_pagina,
        args=("pagina_listar_ofertas",),
    )

    st.sidebar.button(
        "Orçamentos",
        use_container_width=True,
        on_click=mudar_pagina,
        args=("pagina_orcamentos",),
    )

    st.sidebar.button(
        "Relatórios",
        use_container_width=True,
        on_click=mudar_pagina,
        args=("pagina_relatorios",),
    )

    if st.session_state.pagina_atual == "home":
        home()

    elif st.session_state.pagina_atual == "pagina_listar_clientes":
        PageListarClientes.pagina_listar_clientes()

    elif st.session_state.pagina_atual == "pagina_listar_produtos":
        PageListarProdutos.pagina_listar_produtos()

    elif st.session_state.pagina_atual == "pagina_listar_vendedores":
        PageListarVendedores.pagina_listar_vendedores()

    elif st.session_state.pagina_atual == "pagina_listar_ofertas":
        PageListarOfertas.pagina_listar_ofertas()

    elif st.session_state.pagina_atual == "pagina_orcamentos":
        PageListarOrcamentos.pagina_orcamentos()

    elif st.session_state.pagina_atual == "pagina_cadastro_orcamentos":
        PageCadastrarOrcamentos.pagina_cadastro_orcamentos()

    elif st.session_state.pagina_atual == "pagina_relatorios":
        PageRelatorios.pagina_relatorios()


if __name__ == "__main__":
    setup_logging()
    init()
    # cadastrar_dados_fakes()
    main()
