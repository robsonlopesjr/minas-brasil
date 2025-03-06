# Minas Brasil

**Minas Brasil** é uma aplicação web desenvolvida com [Streamlit](https://streamlit.io/) que permite gerenciar clientes, produtos, vendedores, ofertas e orçamentos. A aplicação utiliza um banco de dados SQLite para armazenamento e inclui uma funcionalidade de relatórios para analisar os orçamentos com filtros por período e produto.

## Funcionalidades

- **Clientes:** Cadastro, edição, remoção e listagem de clientes.
- **Produtos:** Cadastro, edição, remoção e listagem de produtos.
- **Vendedores:** Cadastro, edição, remoção e listagem de vendedores.
- **Ofertas:** Criação e gerenciamento de ofertas associadas a produtos, com regras para quantidade a levar e a pagar.
- **Orçamentos:** Criação de orçamentos que relacionam clientes, vendedores e produtos. Cada orçamento é automaticamente registrado com a data de criação.
- **Relatórios:** Geração de um relatório de orçamentos com filtros por período e por produto. O relatório exibe a totalização dos valores por orçamento, os itens detalhados e o total geral de todos os orçamentos.

## Estrutura do Projeto
MinasBrasil/src
├── main.py                        # Ponto de entrada da aplicação; configura a interface e inicializa o banco de dados.
├── routes.py                      # Gerencia a navegação entre as páginas.
├── pages
│   ├── clientes.py                # Interface para gerenciamento de clientes.
│   ├── produtos.py                # Interface para gerenciamento de produtos.
│   ├── vendedores.py              # Interface para gerenciamento de vendedores.
│   ├── ofertas.py                 # Interface para gerenciamento de ofertas.
│   ├── orcamentos.py              # Interface para gerenciamento de orçamentos.
│   ├── orcamentos_cadastro.py     # Interface para criação de orçamentos.
│   └── relatorios.py              # Página para geração de relatórios de orçamentos.
├── controllers
│    ├── ClienteController.py       # Lógica de negócio para clientes.
│    ├── ProdutoController.py       # Lógica de negócio para produtos.
│    ├── VendedorController.py      # Lógica de negócio para vendedores.
│    ├── OfertasController.py       # Lógica de negócio para ofertas.
│    └── OrcamentoController.py     # Lógica de negócio para orçamentos.
└── services
    ├── banco_de_dados.py          # Responsável pela conexão com o SQLite e criação das tabelas (incluindo a data de criação nos orçamentos).
    ├── log.py                     # Configuração do sistema de logging.
    ├── dados_fakers.py            # Gerar dados fakers.

## Pré-requisitos
- Python 3.12 ou superior.
- Streamlit – para a interface web.
- SQLite (já incluso na instalação padrão do Python).

## Instalação
1. Clone o repositório:
```bash
git clone https://github.com/robsonlopesjr/minas-brasil.git
cd minas-brasil
```

2. Crie um ambiente virtual (opcional, mas recomendado):
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```
3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso
1. Execute a aplicação:
```bash
streamlit run main.py
```
2. Acesse a aplicação no navegador:
Geralmente, a aplicação estará disponível em http://localhost:8501.
3. Navegação:
Utilize o menu lateral para acessar as funcionalidades de Clientes, Produtos, Vendedores, Ofertas, Orçamentos e o Relatório de Orçamentos.

##  Banco de Dados
O banco de dados SQLite (prova.db) é criado automaticamente na primeira execução, através da função criar_banco_de_dados() em banco_de_dados.py.

##  Contribuição
Contribuições são bem-vindas! Se desejar melhorar o projeto, sinta-se à vontade para enviar pull requests ou abrir issues para reportar bugs e sugerir novas funcionalidades.

##  Licença
Distribuído sob a licença MIT. Consulte o arquivo LICENSE para mais detalhes.