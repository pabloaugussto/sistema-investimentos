# Sistema de Investimentos Full-Stack

Este é um projeto de um sistema de investimentos onde você pode cadastrar, listar, atualizar e excluir investimentos através de uma API RESTful e uma interface web.

## Funcionalidades

* **Cadastrar investimentos:** Adicione novos investimentos com nome, tipo, valor e data.
* **Listar investimentos:** Visualize todos os investimentos cadastrados em uma tabela.
* **Atualizar investimentos:** Modifique os detalhes de um investimento existente.
* **Excluir investimentos:** Remova investimentos do sistema.

## Tecnologias Usadas

* **Backend:**
    * Python (FastAPI)
    * SQLAlchemy (Banco de Dados SQLite)
    * Uvicorn (Servidor ASGI)
    * Pydantic (Validação de Dados)
* **Frontend:**
    * HTML
    * CSS
    * JavaScript (Vanilla JS)

## Como Rodar o Projeto

1.  **Clone o Repositório:**
    ```bash
    git clone [https://github.com/pabloaugussto/sistema-investimentos.git](https://github.com/pabloaugussto/sistema-investimentos.git)
    cd sistema-investimentos
    ```

2.  **Backend:**
    * Crie e ative um ambiente virtual:
        ```bash
        python -m venv venv
        # Windows: venv\Scripts\activate  |  Linux/macOS: source venv/bin/activate
        ```
    * Instale as dependências (na raiz do projeto):
        ```bash
        pip install -r requirements.txt
        ```
    * Rode o servidor da API:
        ```bash
        python -m uvicorn main:app --reload
        ```
    * O backend estará em `http://127.0.0.1:8000`. A documentação da API em `http://127.0.0.1:8000/docs`.

3.  **Frontend:**
    * Abra o arquivo `frontend/index.html` diretamente no seu navegador.
    * *Alternativa (para melhor experiência):* Se tiver o VS Code com a extensão "Live Server", clique com o botão direito em `frontend/index.html` e selecione "Open with Live Server" (geralmente roda em `http://127.0.0.1:5500`).

Agora você pode acessar a interface web e utilizar o sistema!
