# Sistema de Investimentos

Este é um projeto de um sistema de investimentos onde você pode cadastrar, listar, atualizar e excluir investimentos.

## Funcionalidades

- **Cadastrar investimentos**: Adicione novos investimentos com nome, tipo, valor e data.
- **Listar investimentos**: Visualize todos os investimentos cadastrados.
- **Atualizar investimentos**: Modifique os detalhes de um investimento existente.
- **Excluir investimentos**: Remova investimentos do sistema.

## Como rodar o projeto

1. Clone este repositório para sua máquina local: https://github.com/pabloaugussto/sistema-investimentos.git
2. Instale as dependências:
3. Rode o servidor: uvicorn main:app --reload
4. Acesse o sistema na URL `http://127.0.0.1:8000`.

## Tecnologias usadas

- **Python** (FastAPI)
- **SQLAlchemy** (Banco de dados)
- **Uvicorn** (Servidor ASGI)
- **Pydantic** (Validação de dados)

