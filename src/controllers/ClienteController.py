from services.banco_de_dados import conectar, tabela_existe
import logging


def lista_de_clientes() -> list:
    """
    Retorna uma lista de clientes cadastrados no banco de dados.

    A função realiza as seguintes operações:
    1. Verifica se a tabela "clientes" existe utilizando a função `tabela_existe()`.
       - Se a tabela não existir, um erro é registrado e uma lista vazia é retornada.
    2. Abre uma conexão com o banco de dados utilizando a função `conectar()`.
    3. Cria um cursor para executar a consulta SQL que seleciona todos os clientes,
       ordenando-os pelo campo "nome" em ordem ascendente.
    4. Converte os resultados obtidos (que são do tipo sqlite3.Row) em uma lista de dicionários,
       onde cada dicionário representa um cliente com suas respectivas colunas e valores.
    5. Em caso de qualquer exceção durante a execução, o erro é registrado e uma lista vazia é retornada.

    Retorno:
        list: Uma lista de dicionários representando os clientes cadastrados.
              Retorna uma lista vazia se a tabela não existir ou se ocorrer algum erro durante a consulta.
    """
    if not tabela_existe("clientes"):
        logging.error("Erro: A tabela 'clientes' não existe no banco de dados.")
        return []

    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * from clientes ORDER BY nome ASC")
            clientes = cursor.fetchall()
            return [dict(cliente) for cliente in clientes]
    except Exception as e:
        logging.error(f"Erro ao listar clientes: {e}")


def adicionar_cliente(nome: str) -> None:
    """
    Adiciona um novo cliente na tabela "clientes" do banco de dados.

    A função realiza as seguintes operações:
      1. Abre uma conexão com o banco de dados utilizando a função `conectar()`.
      2. Cria um cursor para executar a consulta SQL.
      3. Executa a instrução INSERT OR IGNORE para inserir o nome do cliente na tabela "clientes".
         - Se o cliente já existir (baseado na restrição UNIQUE), a inserção é ignorada.
      4. Efetua o commit da transação para salvar as alterações.
      5. Registra uma mensagem de sucesso no log.

    Args:
        nome (str): O nome do cliente a ser adicionado.

    Returns:
        None: A função não retorna nenhum valor.

    Raises:
        Exception: Se ocorrer algum erro durante a operação, a exceção é capturada e registrada no log.
    """
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR IGNORE INTO clientes (nome) VALUES (?)",
                (nome,),
            )
            conn.commit()
            logging.info("Cliente adicionado com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao adicionar cliente: {e}")


def atualizar_cliente(codigo: int, nome: str) -> None:
    """
    Atualiza o nome de um cliente na tabela "clientes" do banco de dados.

    Esta função atualiza o registro de um cliente identificado pelo código fornecido,
    definindo um novo valor para o campo "nome". Após a atualização, a transação é confirmada (commit)
    e uma mensagem de sucesso é registrada. Se ocorrer algum erro durante o processo, a exceção é capturada
    e registrada no log.

    Args:
        codigo (int): O código identificador do cliente a ser atualizado.
        nome (str): O novo nome do cliente.

    Returns:
        None

    Raises:
        Exception: Se ocorrer qualquer exceção durante a operação, ela será capturada e registrada no log.
    """
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE clientes SET nome = ? WHERE codigo = ?",
                (nome, codigo),
            )
            conn.commit()
            logging.info("Cliente atualizado com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao atualizar cliente: {e}")


def deletar_cliente(codigo: int) -> None:
    """
    Remove um cliente da tabela "clientes" do banco de dados.

    Esta função remove o registro do cliente identificado pelo código fornecido.
    Após a exclusão, a transação é confirmada (commit) e uma mensagem de sucesso é registrada.
    Em caso de erro, a exceção é capturada e o erro é registrado no log.

    Args:
        codigo (int): O código identificador do cliente a ser removido.

    Returns:
        None

    Raises:
        Exception: Se ocorrer qualquer exceção durante a operação, ela será capturada e registrada no log.
    """
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clientes WHERE codigo = ?", (codigo,))
            conn.commit()
            logging.info("Cliente removido com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao deletar cliente: {e}")
