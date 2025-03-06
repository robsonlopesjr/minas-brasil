from services.banco_de_dados import conectar, tabela_existe
import logging


def lista_de_ofertas() -> list:
    """
    Retorna uma lista de ofertas cadastradas no banco de dados.

    A função realiza as seguintes operações:
      1. Verifica se a tabela "ofertas" existe utilizando a função `tabela_existe()`.
         - Se a tabela não existir, registra um erro e retorna uma lista vazia.
      2. Abre uma conexão com o banco de dados utilizando a função `conectar()`.
      3. Cria um cursor para executar uma consulta SQL que une a tabela "ofertas" com a tabela "produtos".
      4. Converte os resultados (obtidos como objetos do tipo sqlite3.Row) em uma lista de dicionários,
         onde cada dicionário representa uma oferta com seus respectivos dados.

    Returns:
        list: Uma lista de dicionários representando as ofertas cadastradas.
              Retorna uma lista vazia se a tabela "ofertas" não existir ou se ocorrer algum erro durante a consulta.

    Raises:
        Exception: Se ocorrer qualquer exceção durante a operação, ela será capturada e registrada no log.
    """
    if not tabela_existe("ofertas"):
        logging.error("Erro: A tabela 'ofertas' não existe no banco de dados.")
        return []

    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT
                    o.codigo as codigo,
                    o.quantidade_levar as quantidade_levar,
                    o.quantidade_pagar as quantidade_pagar,
                    o.produto_id as produto_id,
                    p.descricao as produto_descricao
                FROM ofertas o
                JOIN produtos p ON p.codigo = o.produto_id
            """
            )
            ofertas = cursor.fetchall()
            return [dict(oferta) for oferta in ofertas]
    except Exception as e:
        logging.error(f"Erro ao listar ofertas: {e}")


def adicionar_oferta(
    produto_id: int, quantidade_levar: int, quantidade_pagar: int
) -> None:
    """
    Adiciona uma nova oferta na tabela "ofertas" do banco de dados.

    A função insere uma nova oferta, associando um produto identificado por `produto_id`
    com as quantidades informadas:
      - `quantidade_levar`: a quantidade que o cliente levará.
      - `quantidade_pagar`: a quantidade que o cliente pagará.
    A inserção utiliza a cláusula "INSERT OR IGNORE", o que significa que se uma oferta
    com os mesmos valores já existir (conforme as restrições da tabela), a inserção será ignorada.

    Args:
        produto_id (int): O identificador do produto associado à oferta.
        quantidade_levar (int): A quantidade de produto que será levada na oferta.
        quantidade_pagar (int): A quantidade de produto que será paga na oferta.

    Returns:
        None

    Raises:
        Exception: Se ocorrer algum erro durante a operação, a exceção é capturada e registrada no log.
    """
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR IGNORE INTO ofertas (produto_id, quantidade_levar, quantidade_pagar) VALUES (?, ?, ?)",
                (produto_id, quantidade_levar, quantidade_pagar),
            )
            conn.commit()
            logging.info("Oferta adicionada com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao adicionar oferta: {e}")


def atualizar_oferta(
    codigo: int, produto_id: int, quantidade_levar: int, quantidade_pagar: int
) -> None:
    """
    Atualiza uma oferta existente na tabela "ofertas" do banco de dados.

    A função atualiza os dados de uma oferta identificada por `codigo`, definindo um novo
    produto associado (`produto_id`) e os valores para `quantidade_levar` e `quantidade_pagar`.
    Após a atualização, a transação é confirmada (commit) e uma mensagem de sucesso é registrada.
    Em caso de erro, a exceção é capturada e o erro é registrado no log.

    Args:
        codigo (int): O código identificador da oferta a ser atualizada.
        produto_id (int): O identificador do novo produto associado à oferta.
        quantidade_levar (int): A nova quantidade a levar na oferta.
        quantidade_pagar (int): A nova quantidade a pagar na oferta.

    Returns:
        None

    Raises:
        Exception: Se ocorrer qualquer exceção durante a operação, ela será capturada e registrada no log.
    """
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE ofertas SET produto_id = ?, quantidade_levar = ?, quantidade_pagar = ? WHERE codigo = ?",
                (produto_id, quantidade_levar, quantidade_pagar, codigo),
            )
            conn.commit()
            logging.info("Oferta atualizada com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao atualizar oferta: {e}")


def deletar_oferta(codigo: int) -> None:
    """
    Remove uma oferta da tabela "ofertas" do banco de dados.

    Esta função remove o registro de uma oferta identificada pelo código fornecido.
    Após a remoção, a transação é confirmada (commit) e uma mensagem de sucesso é registrada.
    Se ocorrer algum erro durante o processo, a exceção é capturada e o erro é registrado no log.

    Args:
        codigo (int): O código identificador da oferta a ser removida.

    Returns:
        None

    Raises:
        Exception: Se ocorrer qualquer exceção durante a operação, ela será capturada e registrada no log.
    """
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM ofertas WHERE codigo = ?", (codigo,))
            conn.commit()
            logging.info("Oferta removida com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao deletar oferta: {e}")
