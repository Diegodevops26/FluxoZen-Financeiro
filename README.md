# FluxoZen Financeiro 🧘‍♂️💰

[![Python](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/sqlalchemy-%23000.svg?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
## Descrição do Projeto

O FluxoZen Financeiro é uma API RESTful desenvolvida em Python utilizando o framework Flask e o ORM SQLAlchemy. Seu objetivo é fornecer uma ferramenta simples e eficiente para o gerenciamento de finanças pessoais, permitindo o controle de transações, categorização de gastos e a geração de relatórios perspicazes para auxiliar na tomada de decisões financeiras.

## Funcionalidades Principais

* **Gerenciamento de Transações:**
    * Criação de novas transações (receitas e despesas) com descrição, valor, data, tipo e categoria.
    * Listagem de todas as transações.
    * Obtenção de detalhes de uma transação específica por ID.
    * Atualização de transações existentes.
    * Exclusão de transações.
* **Gerenciamento de Categorias:**
    * Criação de novas categorias de gastos/receitas com nome (e opcionalmente orçamento).
    * Listagem de todas as categorias.
    * Obtenção de detalhes de uma categoria específica por ID.
    * Atualização de categorias existentes.
    * Exclusão de categorias.
* **Relatórios Financeiros:**
    * **Gastos por Categoria:** Retorna o total gasto por categoria em um período específico (ano e mês).
    * **Comparação de Gastos Mensais:** Compara os gastos totais em um número especificado de meses.
    * **Gastos Recorrentes:** Identifica gastos que ocorrem com frequência em um determinado período.
    * **Comparação com Orçamento:** Compara os gastos com o orçamento definido para cada categoria em um período.
    * **Sugestões de Economia:** Fornece insights e sugestões com base nos dados financeiros.

## Tecnologias Utilizadas

* **Python:** Linguagem de programação principal.
* **Flask:** Microframework web para construção da API RESTful.
* **SQLAlchemy:** ORM (Object-Relational Mapper) para interação com o banco de dados SQLite.
* **SQLite:** Banco de dados leve e fácil de usar para armazenar os dados financeiros.
* **Insomnia/Postman:** (Mencione aqui a ferramenta que você usou para testar a API) Utilizado para testar os endpoints da API.

## Pré-requisitos

* **Python 3.x** instalado no seu sistema.
* **Pip** (Python package installer) instalado.

## Instalação

1.  **Clone o repositório:**
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd fluxozen-financeiro
    ```

2.  **Crie um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Linux/macOS
    venv\Scripts\activate  # No Windows
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Você precisará criar um arquivo `requirements.txt` listando as dependências: `Flask`, `SQLAlchemy`, `Flask-Migrate` (se você usou migrations))*

4.  **Execute a aplicação:**
    ```bash
    python app.py
    ```
    A API estará disponível em `http://127.0.0.1:5000`.

## Documentação da API (Endpoints)

Aqui você deve listar todos os seus endpoints com detalhes sobre:

* **Endpoint:** A URL do endpoint.
* **Método HTTP:** (GET, POST, PUT, DELETE).
* **Parâmetros (se houver):**
    * **Path Parameters:** (Ex: `/transacoes/<int:id>`). Explique o propósito e o tipo.
    * **Query Parameters:** (Ex: `/relatorios/gastos_por_categoria?ano=2025&mes=4`). Explique o nome, tipo, se é obrigatório e o seu propósito.
* **Corpo da Requisição (para POST e PUT):** Especifique o formato (JSON) e os campos esperados (nome, tipo, descrição, se são obrigatórios, exemplos).
* **Respostas:**
    * **Códigos de Status:** (Ex: 200 OK, 201 Created, 400 Bad Request, 404 Not Found, 409 Conflict).
    * **Corpo da Resposta (JSON):** Descreva a estrutura do JSON retornado para cada código de status (campos, tipos, exemplos).

**Exemplo de documentação de um endpoint:**

### `POST /transacoes`

* **Método HTTP:** `POST`
* **Descrição:** Cria uma nova transação.
* **Corpo da Requisição (JSON):**
    ```json
    {
        "descricao": "Almoço no restaurante",
        "valor": 55.90,
        "tipo": "despesa",
        "categoria_id": 1,
        "data": "2025-05-05T12:00:00" (opcional, padrão é a data e hora atual)
    }
    ```
    * `descricao` (string, obrigatório): Descrição da transação.
    * `valor` (number, obrigatório): Valor da transação.
    * `tipo` (string, obrigatório): Tipo da transação ('receita' ou 'despesa').
    * `categoria_id` (integer, obrigatório): ID da categoria à qual a transação pertence.
    * `data` (string, opcional): Data e hora da transação no formato ISO 8601.
* **Respostas:**
    * **`201 Created`:**
        ```json
        {
            "message": "Transação criada com sucesso!",
            "id": 5
        }
        ```
    * **`400 Bad Request`:** Retorna uma mensagem de erro se os dados da requisição forem inválidos.
        ```json
        {
            "message": "Dados inválidos"
        }
        ```
    * **`404 Not Found`:** Retorna uma mensagem se a `categoria_id` não existir.
        ```json
        {
            "message": "Categoria não encontrada"
        }
        ```

Continue documentando todos os seus endpoints (GET `/transacoes`, GET `/transacoes/<id>`, PUT `/transacoes/<id>`, DELETE `/transacoes/<id>`, e todos os endpoints de categorias e relatórios) seguindo este formato.

## Contribuição

Se você quiser contribuir para este projeto, sinta-se à vontade para abrir issues para relatar bugs ou sugerir novas funcionalidades. Pull requests são bem-vindos!

## Licença

Este projeto está sob a licença [MIT](https://opensource.org/licenses/MIT).

## Autor

[DiegoSantos.Dev]

---



