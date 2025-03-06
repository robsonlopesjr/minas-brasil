from services.banco_de_dados import conectar, tabela_existe
import logging


def lista_de_produtos() -> list:
    """
    Retorna uma lista de produtos cadastrados na tabela "produtos" do banco de dados.

    A função realiza as seguintes operações:
      1. Verifica se a tabela "produtos" existe utilizando a função `tabela_existe()`.
         Se a tabela não existir, registra um erro e retorna uma lista vazia.
      2. Abre uma conexão com o banco de dados utilizando a função `conectar()`.
      3. Cria um cursor para executar uma consulta SQL que seleciona todos os produtos,
         ordenando-os pela coluna "descricao" em ordem ascendente.
      4. Converte os resultados (obtidos como objetos do tipo sqlite3.Row) em uma lista de dicionários,
         onde cada dicionário representa um produto com suas respectivas colunas e valores.

    Returns:
        list: Uma lista de dicionários representando os produtos cadastrados.
              Retorna uma lista vazia se a tabela "produtos" não existir ou se ocorrer algum erro durante a consulta.
    """
    if not tabela_existe("produtos"):
        logging.error("Erro: A tabela 'produtos' não existe no banco de dados.")
        return []

    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * from produtos ORDER BY descricao ASC")
            produtos = cursor.fetchall()
            return [dict(produto) for produto in produtos] if produtos else []
    except Exception as e:
        logging.error(f"Erro ao listar produtos: {e}")
        return []


def adicionar_produto(descricao: str, preco: float) -> None:
    """
    Adiciona um novo produto na tabela "produtos" do banco de dados.

    A função insere um novo registro na tabela "produtos" utilizando a descrição e o preço fornecidos.
    Se um produto com a mesma descrição já existir (conforme restrição UNIQUE), a inserção será ignorada
    devido ao uso do comando "INSERT OR IGNORE".

    Args:
        descricao (str): A descrição do produto.
        preco (float): O preço do produto.

    Returns:
        None

    Raises:
        Exception: Se ocorrer algum erro durante a operação de inserção, a exceção será capturada e
                   o erro será registrado no log.
    """
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR IGNORE INTO produtos (descricao, preco) VALUES (?, ?)",
                (descricao, preco),
            )
            conn.commit()
            logging.info("Produto adicionado com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao adicionar produto: {e}")


def atualizar_produto(codigo: int, descricao: str, preco: float) -> None:
    """
    Atualiza as informações de um produto na tabela "produtos" do banco de dados.

    Esta função atualiza a descrição e o preço de um produto identificado pelo código fornecido.
    Após a atualização, a transação é confirmada (commit) e uma mensagem de sucesso é registrada no log.
    Se ocorrer qualquer erro durante o processo, a exceção é capturada e o erro é registrado no log.

    Args:
        codigo (int): O código identificador do produto a ser atualizado.
        descricao (str): A nova descrição do produto.
        preco (float): O novo preço do produto.

    Returns:
        None

    Raises:
        Exception: Se ocorrer algum erro durante a operação, a exceção será capturada e registrada no log.
    """
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE produtos SET descricao = ?, preco = ? WHERE codigo = ?",
                (descricao, preco, codigo),
            )
            conn.commit()
            logging.info("Produto atualizado com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao atualizar produto: {e}")


def deletar_produto(codigo: int) -> None:
    """
    Remove um produto da tabela "produtos" do banco de dados.

    Esta função remove o registro do produto identificado pelo código fornecido.
    Após a exclusão, a transação é confirmada (commit) e uma mensagem de sucesso é registrada no log.
    Em caso de erro, a exceção é capturada e o erro é registrado no log.

    Args:
        codigo (int): O código identificador do produto a ser removido.

    Returns:
        None

    Raises:
        Exception: Se ocorrer qualquer erro durante a operação, a exceção será capturada e registrada no log.
    """
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM produtos WHERE codigo = ?", (codigo,))
            conn.commit()
            logging.info("Produto removido com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao deletar produto: {e}")
