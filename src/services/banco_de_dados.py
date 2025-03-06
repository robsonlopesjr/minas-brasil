import sqlite3
import os
import logging


def conectar():
    conn = sqlite3.connect("prova.db")
    conn.row_factory = sqlite3.Row

    return conn


def criar_tabela_clientes(conn):
    sql = """
        CREATE TABLE IF NOT EXISTS clientes (
            codigo INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL
        )
    """
    conn.execute(sql)
    conn.commit()


def criar_tabela_produtos(conn):
    sql = """
        CREATE TABLE IF NOT EXISTS produtos (
            codigo INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT UNIQUE NOT NULL,
            preco NUMERIC NOT NULL
        )
    """
    conn.execute(sql)
    conn.commit()


def criar_tabela_vendedores(conn):
    sql = """
        CREATE TABLE IF NOT EXISTS vendedores (
            codigo INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL
        )
    """
    conn.execute(sql)
    conn.commit()


def criar_tabela_ofertas(conn):
    sql = """
        CREATE TABLE IF NOT EXISTS ofertas (
            codigo INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER UNIQUE NOT NULL,
            quantidade_levar INTEGER NOT NULL CHECK (quantidade_levar > 0),
            quantidade_pagar INTEGER NOT NULL CHECK (quantidade_pagar > 0 AND quantidade_pagar < quantidade_levar),
            FOREIGN KEY (produto_id) REFERENCES produtos (id) ON DELETE CASCADE
        )
    """
    conn.execute(sql)
    conn.commit()


def criar_tabela_orcamentos(conn):
    sql = """
        CREATE TABLE IF NOT EXISTS orcamentos (
            codigo INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            vendedor_id INTEGER NOT NULL,
            data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (cliente_id) REFERENCES clientes (id) ON DELETE CASCADE,
            FOREIGN KEY (vendedor_id) REFERENCES vendedores (id) ON DELETE CASCADE
        )
    """
    conn.execute(sql)
    conn.commit()


def criar_tabela_orcamento_itens(conn):
    sql = """
        CREATE TABLE IF NOT EXISTS orcamento_itens (
            codigo INTEGER PRIMARY KEY AUTOINCREMENT,
            orcamento_id INTEGER NOT NULL,
            produto_id INTEGER NOT NULL,
            quantidade INTEGER NOT NULL,
            preco_unitario NUMERIC NOT NULL,
            desconto NUMERIC NOT NULL,
            FOREIGN KEY (orcamento_id) REFERENCES orcamentos (id) ON DELETE CASCADE,
            FOREIGN KEY (produto_id) REFERENCES produtos (id) ON DELETE CASCADE
        )
    """
    conn.execute(sql)
    conn.commit()


def criar_banco_de_dados() -> None:
    """
    Cria o banco de dados e as tabelas necessárias se o arquivo "prova.db" não existir.

    A função verifica se o arquivo "prova.db" já existe. Caso não exista, ela:
      1. Abre uma conexão com o banco de dados utilizando a função `conectar()`.
      2. Cria as tabelas necessárias chamando as funções:
           - criar_tabela_clientes(conn)
           - criar_tabela_produtos(conn)
           - criar_tabela_vendedores(conn)
           - criar_tabela_ofertas(conn)
           - criar_tabela_orcamentos(conn)
           - criar_tabela_orcamento_itens(conn)
      3. Registra uma mensagem de sucesso no log informando que o banco de dados e as tabelas foram criados.

    Se ocorrer um erro durante o processo de criação do banco de dados (capturado como `sqlite3.Error`),
    o erro será registrado no log.

    Returns:
        None
    """
    if not os.path.exists("prova.db"):
        try:
            with conectar() as conn:
                criar_tabela_clientes(conn)
                criar_tabela_produtos(conn)
                criar_tabela_vendedores(conn)
                criar_tabela_ofertas(conn)
                criar_tabela_orcamentos(conn)
                criar_tabela_orcamento_itens(conn)
                logging.info("Banco de dados e tabelas criados com sucesso.")
        except sqlite3.Error as e:
            logging.error(f"Erro ao criar banco de dados: {e}")


def tabela_existe(nome_tabela: str) -> bool:
    """
    Verifica se uma tabela específica existe no banco de dados SQLite.

    A função executa uma consulta na tabela interna "sqlite_master" para verificar se existe
    uma tabela com o nome fornecido. Retorna True se a tabela existir, caso contrário, retorna False.

    Args:
        nome_tabela (str): O nome da tabela a ser verificada.

    Returns:
        bool: True se a tabela existir, False caso contrário.

    Raises:
        Exception: Se ocorrer um erro durante a verificação, o erro será registrado no log e
                   a função retornará False.
    """
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                (nome_tabela,),
            )
            return cursor.fetchone() is not None  # Retorna True se a tabela existir
    except Exception as e:
        logging.error(f"Erro ao verificar existência da tabela {nome_tabela}: {e}")
        return False
