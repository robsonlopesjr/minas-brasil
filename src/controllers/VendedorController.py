from services.banco_de_dados import conectar, tabela_existe
import logging


def lista_de_vendedores() -> list:
    """
    Retorna uma lista de vendedores cadastrados na tabela "vendedores" do banco de dados.

    A função executa as seguintes etapas:
      1. Verifica se a tabela "vendedores" existe utilizando a função `tabela_existe()`.
         Se a tabela não existir, registra um erro e retorna uma lista vazia.
      2. Abre uma conexão com o banco de dados utilizando a função `conectar()`.
      3. Cria um cursor para executar uma consulta SQL que seleciona todos os registros
         da tabela "vendedores", ordenados pelo campo "nome" em ordem ascendente.
      4. Converte os resultados, obtidos como objetos do tipo sqlite3.Row, em uma lista de dicionários,
         onde cada dicionário representa um vendedor com suas respectivas colunas e valores.

    Returns:
        list: Uma lista de dicionários representando os vendedores cadastrados.
              Retorna uma lista vazia se a tabela "vendedores" não existir ou se ocorrer algum erro durante a consulta.
    """
    if not tabela_existe("vendedores"):
        logging.error("Erro: A tabela 'vendedores' não existe no banco de dados.")
        return []

    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * from vendedores ORDER BY nome ASC")
            vendedores = cursor.fetchall()
            return [dict(vendedor) for vendedor in vendedores]
    except Exception as e:
        logging.error(f"Erro ao listar vendedores: {e}")


def adicionar_vendedor(nome: str) -> None:
    """
    Adiciona um novo vendedor na tabela "vendedores" do banco de dados.

    Esta função insere um novo registro na tabela "vendedores" utilizando o nome fornecido.
    Se um vendedor com o mesmo nome já existir (devido à restrição UNIQUE), a inserção será ignorada
    graças ao comando "INSERT OR IGNORE".

    Args:
        nome (str): O nome do vendedor a ser adicionado.

    Returns:
        None

    Raises:
        Exception: Se ocorrer algum erro durante a operação de inserção, a exceção é capturada e
                   o erro é registrado no log.
    """
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR IGNORE INTO vendedores (nome) VALUES (?)",
                (nome,),
            )
            conn.commit()
            logging.info("Vendedor adicionado com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao adicionar vendedor: {e}")


def atualizar_vendedor(codigo: int, nome: str) -> None:
    """
    Atualiza o nome de um vendedor na tabela "vendedores" do banco de dados.

    Esta função atualiza o registro de um vendedor identificado pelo código fornecido, 
    definindo um novo nome para o vendedor. Após a atualização, a transação é confirmada (commit) 
    e uma mensagem de sucesso é registrada no log. Caso ocorra algum erro durante o processo, 
    a exceção é capturada e o erro é registrado no log.

    Args:
        codigo (int): O código identificador do vendedor a ser atualizado.
        nome (str): O novo nome do vendedor.

    Returns:
        None

    Raises:
        Exception: Se ocorrer qualquer erro durante a operação, a exceção será capturada 
                   e registrada no log.
    """
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE vendedores SET nome = ? WHERE codigo = ?",
                (nome, codigo),
            )
            conn.commit()
            logging.info("Vendedor atualizado com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao atualizar vendedor: {e}")


def deletar_vendedor(codigo: int) -> None:
    """
    Remove um vendedor da tabela "vendedores" do banco de dados.

    Esta função remove o registro do vendedor identificado pelo código fornecido.
    Após a exclusão, a transação é confirmada (commit) e uma mensagem de sucesso é registrada no log.
    Em caso de erro, a exceção é capturada e o erro é registrado no log.

    Args:
        codigo (int): O código identificador do vendedor a ser removido.

    Returns:
        None

    Raises:
        Exception: Se ocorrer qualquer erro durante a operação, a exceção será capturada e registrada no log.
    """
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM vendedores WHERE codigo = ?", (codigo,))
            conn.commit()
            logging.info("Vendedor removido com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao deletar vendedor: {e}")
