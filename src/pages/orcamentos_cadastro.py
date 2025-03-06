import streamlit as st
import pandas as pd
from controllers.OrcamentoController import adicionar_orcamento
from controllers.ProdutoController import lista_de_produtos
from controllers.ClienteController import lista_de_clientes
from controllers.VendedorController import lista_de_vendedores
from controllers.OfertasController import lista_de_ofertas
from routes import mudar_pagina


orcamento_produtos = []


# Função para adicionar produtos ao orçamento
@st.dialog("Adicionar Produto ao Orçamento")
def adicionar_produto(produtos_dict, ofertas_dict):
    with st.form("form_add_produto", clear_on_submit=True):
        produto_escolhido = st.selectbox("Produto", list(produtos_dict.keys()))
        quantidade = st.number_input("Quantidade", min_value=1, step=1)

        submitted = st.form_submit_button(label="Adicionar", type="primary")

        if submitted:
            produto = produtos_dict[produto_escolhido]
            preco_unitario = produto["preco"]
            total = preco_unitario * quantidade

            # Verifica se existe uma oferta para esse produto
            desconto = 0
            if produto["codigo"] in ofertas_dict:
                oferta = ofertas_dict[produto["codigo"]]
                qtd_levar = oferta["quantidade_levar"]
                qtd_pagar = oferta["quantidade_pagar"]

                # Calcula a quantidade de grupos da oferta
                grupos = quantidade // qtd_levar
                restante = quantidade % qtd_levar

                # Preço real baseado na oferta
                total = (grupos * qtd_pagar * preco_unitario) + (
                    restante * preco_unitario
                )
                desconto = grupos * (qtd_levar - qtd_pagar) * preco_unitario

            orcamento_produtos.append(
                {
                    "Código": produto["codigo"],
                    "Produto": produto["descricao"],
                    "Quantidade": quantidade,
                    "Preço Unitário": f"R$ {preco_unitario:.2f}",
                    "Desconto": f"R$ {desconto:.2f}",
                    "Total": f"R$ {total:.2f}",
                }
            )
            st.rerun()


def pagina_cadastro_orcamentos():
    st.button(
        label="Listar Orçamento",
        key="btn_incluir",
        type="primary",
        on_click=mudar_pagina,
        args=("pagina_orcamentos",),
    )
    # Interface de seleção de vendedor e cliente
    st.header("Criar Orçamento", divider=True)
    # Obtendo dados do banco
    clientes = lista_de_clientes()
    vendedores = lista_de_vendedores()
    produtos = lista_de_produtos()
    ofertas = lista_de_ofertas()

    if not clientes or not vendedores or not produtos or not ofertas:
        st.info(
            "Faltam dados essenciais. Cadastre clientes, vendedores, produtos e ofertas antes de continuar."
        )
    else:

        # Criando dicionários para facilitar buscas
        clientes_dict = {cliente["nome"]: cliente["codigo"] for cliente in clientes}
        vendedores_dict = {
            vendedor["nome"]: vendedor["codigo"] for vendedor in vendedores
        }
        produtos_dict = {produto["descricao"]: produto for produto in produtos}

        # Criando dicionário de ofertas
        ofertas_dict = {}
        for oferta in ofertas:
            ofertas_dict[oferta["produto_id"]] = {
                "quantidade_levar": oferta["quantidade_levar"],
                "quantidade_pagar": oferta["quantidade_pagar"],
            }

        vendedor_nome = st.selectbox(
            "Selecione o Vendedor", list(vendedores_dict.keys()), key="vendedor"
        )
        cliente_nome = st.selectbox(
            "Selecione o Cliente", list(clientes_dict.keys()), key="cliente"
        )

        # Regra: Vendedor não pode ser cliente ao mesmo tempo
        if vendedor_nome == cliente_nome:
            st.error("O vendedor não pode ser o mesmo que o cliente!")
            st.stop()

        # Botão para adicionar produtos
        if st.button("Adicionar Produto", type="primary"):
            adicionar_produto(produtos_dict, ofertas_dict)

        # Exibe produtos adicionados ao orçamento
        st.subheader("Itens do Orçamento")
        if not orcamento_produtos:
            st.info("Nenhum produto adicionado ainda.")
        else:
            df_orcamento = pd.DataFrame(orcamento_produtos)
            st.dataframe(df_orcamento, hide_index=True, use_container_width=True)

            total_final = sum(
                float(produto["Total"].replace("R$", "").strip())
                for produto in orcamento_produtos
            )
            st.markdown(f"### Total do Orçamento: R$ {total_final:.2f}")

            # Botão para salvar o orçamento no banco de dados
            if st.button("Salvar Orçamento", type="primary"):
                if vendedor_nome == cliente_nome:
                    st.warning("O vendedor não pode ser cliente ao mesmo tempo.")
                    return
                else:
                    adicionar_orcamento(
                        cliente_id=clientes_dict[cliente_nome],
                        vendedor_id=vendedores_dict[vendedor_nome],
                        itens=orcamento_produtos,
                    )
                    orcamento_produtos.clear()
                    st.success("Orçamento salvo com sucesso!")
                    mudar_pagina("pagina_orcamentos")
                    st.rerun()
