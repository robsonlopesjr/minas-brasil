import streamlit as st
from controllers.OrcamentoController import lista_de_orcamentos, deletar_orcamento
from routes import mudar_pagina


def pagina_orcamentos():
    st.button(
        label="Adicionar Orçamento",
        key="btn_incluir",
        type="primary",
        on_click=mudar_pagina,
        args=("pagina_cadastro_orcamentos",),
    )
    st.header("Listagem de Orcamentos", divider=True)

    orcamentos = lista_de_orcamentos()

    if not orcamentos:
        st.info("Não há orçamentos cadastrados")
    else:
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.write("CLIENTE")
        col2.write("VENDEDOR")
        col3.write("VALOR DO ORÇAMENTO")
        col4.write("DESCONTO")

        for orcamento in orcamentos:
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.write(orcamento["nome_cliente"])
            col2.write(orcamento["nome_vendedor"])
            col3.write(f"R${orcamento['valor_itens']:.2f}")
            col4.write(f"R${orcamento["desconto"]:.2f}")
            if col5.button(
                label="Remover",
                key=f"remover_{orcamento['codigo']}",
                use_container_width=True,
            ):
                deletar_orcamento(orcamento["codigo"])
                st.rerun()
