import streamlit as st
from controllers.ProdutoController import lista_de_produtos
from controllers.OrcamentoController import gerar_relatorio
from datetime import date


def pagina_relatorios():
    st.header("Relatório de Orçamentos", divider=True)
    st.subheader("Filtros")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        data_inicio = st.date_input("Data Início", value=date.today())
    with col2:
        data_fim = st.date_input("Data Fim", value=date.today())
    with col3:
        produtos = lista_de_produtos()
        if produtos:
            opcoes_produto = {"Todos": -1}
            for produto in produtos:
                opcoes_produto[produto["descricao"]] = produto["codigo"]

            produto_selecionado = st.selectbox("Produto", list(opcoes_produto.keys()))
            produto_codigo = opcoes_produto[produto_selecionado]
    with col4:
        botao_gerar_relatorio = st.button("Gerar Relatório")
        
    if botao_gerar_relatorio:
        df = gerar_relatorio(data_inicio.isoformat(), data_fim.isoformat(), produto_codigo)

        if df.empty:
            st.info("Nenhum orçamento encontrado para os filtros selecionados.")
        else:
            df_orcamento = (
                df.groupby(["orcamento_id", "nome_cliente", "nome_vendedor", "data_criacao"])["total_item"]
                .sum()
                .reset_index()
                .rename(columns={"total_item": "total_orcamento"})
            )

            st.subheader("Totalização por Orçamento")
            st.dataframe(df_orcamento, use_container_width=True)
            
            total_geral = df_orcamento["total_orcamento"].sum()
            st.markdown(f"### Total Geral dos Orçamentos: R$ {total_geral:.2f}")
            
            st.subheader("Itens dos Orçamentos")
            st.dataframe(df, use_container_width=True)