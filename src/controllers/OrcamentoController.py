import logging
import pandas as pd
from services.banco_de_dados import conectar


def lista_de_orcamentos() -> list:
    """
    Retorna uma lista de orçamentos agregados a partir do banco de dados.

    A função executa uma consulta SQL que junta as tabelas "orcamentos", "clientes",
    "vendedores" e "orcamento_itens" para calcular os seguintes campos:
      - "codigo": Código identificador do orçamento.
      - "nome_cliente": Nome do cliente associado ao orçamento.
      - "nome_vendedor": Nome do vendedor associado ao orçamento.
      - "valor_itens": Soma dos valores dos itens do orçamento, calculada como (quantidade * preco_unitario).
      - "desconto": Soma dos descontos aplicados aos itens do orçamento.

    Os resultados são agrupados pelo código do orçamento, nome do cliente e nome do vendedor.

    Returns:
        list: Uma lista de dicionários, onde cada dicionário contém os campos:
              "codigo", "nome_cliente", "nome_vendedor", "valor_itens" e "desconto".
              Se ocorrer um erro durante a execução da consulta, a função retorna uma lista vazia.

    Raises:
        Exception: Se ocorrer alguma exceção durante a execução da consulta, o erro será registrado no log.
    """
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT
                    o.codigo as codigo,
                    c.nome as nome_cliente,
                    v.nome as nome_vendedor,
                    SUM(i.quantidade * i.preco_unitario) as valor_itens,
                    SUM(i.desconto) as desconto
                FROM orcamentos o
                JOIN clientes c ON c.codigo = o.cliente_id
                JOIN vendedores v ON v.codigo = o.vendedor_id
                JOIN orcamento_itens i ON i.orcamento_id = o.codigo
                GROUP BY o.codigo, c.nome, v.nome
            """
            )
            orcamentos = cursor.fetchall()
            return [dict(orcamento) for orcamento in orcamentos]
    except Exception as e:
        logging.error(f"Erro ao listar orcamentos: {e}")


def adicionar_orcamento(cliente_id: int, vendedor_id: int, itens: list) -> None:
    """
    Adiciona um novo orçamento e seus itens correspondentes no banco de dados.

    Esta função realiza as seguintes operações:
      1. Insere um novo registro na tabela "orcamentos", associando um cliente e um vendedor.
         A inserção utiliza "INSERT OR IGNORE", o que significa que se o registro já existir,
         a operação será ignorada.
      2. Obtém o ID do orçamento recém-criado (orcamento_id).
      3. Para cada item presente na lista `itens`, insere um registro na tabela "orcamento_itens"
         contendo:
            - orcamento_id: o ID do orçamento criado.
            - produto_id: o identificador do produto (extraído do campo "Código" do item).
            - quantidade: a quantidade do produto (campo "Quantidade").
            - preco_unitario: o preço unitário, convertido de string formatada (ex: "R$ 12.34")
              para float.
            - desconto: o desconto aplicado, convertido de string formatada (ex: "R$ 2.34") para float.
      4. Efetua o commit da transação para salvar as inserções.
      5. Registra uma mensagem de sucesso ou, em caso de exceção, registra o erro no log.

    Args:
        cliente_id (int): Identificador do cliente associado ao orçamento.
        vendedor_id (int): Identificador do vendedor associado ao orçamento.
        itens (list): Lista de dicionários, onde cada dicionário representa um item do orçamento e
                      deve conter as seguintes chaves:
                          - "Código" (int): Identificador do produto.
                          - "Quantidade" (int): Quantidade do produto.
                          - "Preço Unitário" (str): Preço unitário formatado (ex: "R$ 12.34").
                          - "Desconto" (str): Desconto formatado (ex: "R$ 2.34").

    Returns:
        None

    Raises:
        Exception: Se ocorrer algum erro durante a inserção do orçamento ou dos seus itens,
                   a exceção é capturada e o erro é registrado no log.
    """
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR IGNORE INTO orcamentos (cliente_id, vendedor_id) VALUES (?, ?)",
                (cliente_id, vendedor_id),
            )

            orcamento_id = cursor.lastrowid

            for item in itens:
                cursor.execute(
                    """
                    INSERT OR IGNORE INTO orcamento_itens (orcamento_id, produto_id, quantidade, preco_unitario, desconto)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        orcamento_id,
                        item["Código"],
                        item["Quantidade"],
                        float(item["Preço Unitário"].replace("R$", "").strip()),
                        float(item["Desconto"].replace("R$", "").strip()),
                    ),
                )

            conn.commit()
            logging.info("orcamento adicionada com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao adicionar orcamento: {e}")


def deletar_orcamento(codigo: int) -> None:
    """
    Remove um orçamento e seus itens associados do banco de dados.

    A função realiza as seguintes operações:
      1. Abre uma conexão com o banco de dados utilizando a função `conectar()`.
      2. Remove todos os registros da tabela "orcamento_itens" que estejam associados
         ao orçamento identificado por `codigo`, garantindo que os itens relacionados sejam excluídos.
      3. Remove o registro do orçamento da tabela "orcamentos" com o código especificado.
      4. Efetua o commit da transação para confirmar as alterações no banco de dados.
      5. Registra uma mensagem de sucesso no log. Se ocorrer algum erro, a exceção é capturada
         e o erro é registrado no log.

    Args:
        codigo (int): O código identificador do orçamento a ser removido.

    Returns:
        None

    Raises:
        Exception: Se ocorrer qualquer erro durante o processo de deleção, a exceção será
                   capturada e registrada no log.
    """
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM orcamento_itens WHERE orcamento_id = ?", (codigo,)
            )
            cursor.execute("DELETE FROM orcamentos WHERE codigo = ?", (codigo,))
            conn.commit()
            logging.info("orcamento removido com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao deletar orcamento: {e}")


def gerar_relatorio(
    data_inicio: str, data_fim: str, produto_codigo: int = -1
) -> pd.DataFrame:
    """
    Gera um relatório de orçamentos filtrado por período e, opcionalmente, por produto.

    Esta função executa uma consulta SQL que retorna um DataFrame contendo informações detalhadas
    sobre os orçamentos, incluindo:
      - orcamento_id: Código identificador do orçamento.
      - data_criacao: Data em que o orçamento foi criado.
      - nome_cliente: Nome do cliente associado ao orçamento.
      - nome_vendedor: Nome do vendedor associado ao orçamento.
      - produto: Descrição do produto presente no orçamento.
      - quantidade: Quantidade do produto orçado.
      - preco_unitario: Preço unitário do produto.
      - desconto: Desconto aplicado ao item.
      - total_item: Total calculado para o item, definido como (quantidade * preco_unitario - desconto).

    Os filtros aplicados são:
      - Período: A data de criação (data_criacao) do orçamento é filtrada entre data_inicio e data_fim.
        A função DATE() do SQLite é utilizada para comparar apenas a parte da data.
      - Produto: Se o parâmetro produto_codigo for diferente de -1, a consulta será filtrada para incluir
        apenas os orçamentos que contenham o produto com o código especificado.

    Args:
        data_inicio (str): Data de início do filtro, no formato "YYYY-MM-DD".
        data_fim (str): Data final do filtro, no formato "YYYY-MM-DD".
        produto_codigo (int, optional): Código do produto para filtrar os orçamentos.
                                        Se for -1, o filtro por produto não é aplicado.
                                        Padrão é -1.

    Returns:
        pd.DataFrame: Um DataFrame contendo os resultados da consulta. As colunas retornadas incluem:
                      'orcamento_id', 'data_criacao', 'nome_cliente', 'nome_vendedor', 'produto',
                      'quantidade', 'preco_unitario', 'desconto' e 'total_item'.

    Raises:
        Exception: Se ocorrer algum erro durante a execução da consulta, o erro é registrado no log.
    """
    query = """
            SELECT
                o.codigo as orcamento_id,
                o.data_criacao,
                c.nome as nome_cliente,
                v.nome as nome_vendedor,
                p.descricao as produto,
                i.quantidade,
                i.preco_unitario,
                i.desconto,
                (i.quantidade * i.preco_unitario - i.desconto) as total_item
            FROM orcamentos o
            JOIN clientes c ON c.codigo = o.cliente_id
            JOIN vendedores v ON v.codigo = o.vendedor_id
            JOIN orcamento_itens i ON i.orcamento_id = o.codigo
            JOIN produtos p ON p.codigo = i.produto_id
            WHERE DATE(o.data_criacao) BETWEEN ? AND ?
            """
    params = [data_inicio, data_fim]
    if produto_codigo != -1:
        query += " AND p.codigo = ?"
        params.append(produto_codigo)
    query += " ORDER BY o.codigo"
    try:
        with conectar() as conn:
            df = pd.read_sql_query(query, conn, params=params)
            return df
    except Exception as e:
        logging.error(f"Erro ao listar clientes: {e}")
