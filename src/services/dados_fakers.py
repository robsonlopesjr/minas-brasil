from controllers.ClienteController import adicionar_cliente
from controllers.ProdutoController import adicionar_produto
from controllers.VendedorController import adicionar_vendedor
from controllers.OfertasController import adicionar_oferta
import logging


def cadastrar_dados_fakes():
    try:
        logging.warning("==========INSERINDO DADOS FAKES==========")
        adicionar_cliente("Gregório de Matos")
        adicionar_cliente("Gonçalves Dias")
        adicionar_cliente("Álvares de Azevedor")
        adicionar_cliente("Castro Alves")
        adicionar_cliente("José de Alencar")
        adicionar_cliente("Olavo Bilac")
        adicionar_produto("Epocler Sabor Abacaxi Flaconete Com 10ml", 3.10)
        adicionar_produto("Engov Com 6 Comprimidos", 7.00)
        adicionar_produto("Doralgina Com 20 Drágeas", 8.90)
        adicionar_produto("Histamin 2Mg C/ 20 Comprimidos", 5.90)
        adicionar_produto("Neosoro Solução Nasal Adulto Com 30 Ml", 4.99)
        adicionar_produto("Dormec Infantil 100Mg Com 10 Comprimidos", 1.33)
        adicionar_vendedor("Jason Statham")
        adicionar_vendedor("Adam Sandler")
        adicionar_vendedor("Castro Alves")
        adicionar_vendedor("Dwayne Johnson")
        adicionar_vendedor("Johnny Depp")
        adicionar_vendedor("Will Smith")
        adicionar_vendedor("Jennifer Lawrence")
        adicionar_oferta(3, 2, 1)
        adicionar_oferta(6, 4, 1)
        adicionar_oferta(2, 6, 3)
        logging.warning("==========TERMINOU DE INSERIR DADOS FAKES==========")
    except Exception as e:
        logging.error(f"Erro ao inserir dados fakes: {e}")
