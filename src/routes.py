import streamlit as st


def mudar_pagina(nome_pagina: str) -> None:
    """
    Altera a página atual da aplicação configurando o estado da sessão.

    Esta função atualiza a chave 'pagina_atual' no objeto de estado da sessão do Streamlit,
    definindo-a como o nome da página fornecido. Essa alteração permite a navegação entre
    diferentes páginas da aplicação.

    Args:
        nome_pagina (str): O nome da página para a qual a navegação deve ocorrer.

    Returns:
        None
    """
    st.session_state.pagina_atual = nome_pagina
