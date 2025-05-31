# 💸 Sistema de Investimentos Full-Stack

Sistema completo para gerenciamento de investimentos pessoais. Com ele, você pode adicionar, visualizar, editar e remover investimentos por meio de uma **API RESTful** construída com **FastAPI** e uma **interface web** simples e funcional.

---

## ✅ Funcionalidades

- **Cadastrar investimentos:** Adicione novos investimentos com nome, tipo, valor e data.
- **Listar investimentos:** Visualize todos os investimentos cadastrados em uma tabela.
- **Atualizar investimentos:** Modifique os detalhes de um investimento existente.
- **Excluir investimentos:** Remova investimentos do sistema.

---

## 🛠 Tecnologias Usadas

### Backend:
- Python (FastAPI)
- SQLAlchemy (Banco de Dados SQLite)
- Uvicorn (Servidor ASGI)
- Pydantic (Validação de Dados)

### Frontend:
- HTML
- CSS
- JavaScript

---

## 📋 Pré-requisitos

Antes de começar, você precisa ter instalado em sua máquina:
- [Python 3.8+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/) (opcional, mas recomendado)

---

## 🚀 Como Rodar o Projeto

1. **Clone o Repositório:**
   ```bash
   git clone https://github.com/pabloaugussto/sistema-investimentos.git
   cd sistema-investimentos
   ```

2. **Backend:**
   - Crie e ative um ambiente virtual:
     ```bash
     python -m venv venv
     # Windows: venv\Scripts\activate
     # Linux/macOS: source venv/bin/activate
     ```
   - Instale as dependências:
     ```bash
     pip install -r requirements.txt
     ```
   - Inicie o servidor:
     ```bash
     python -m uvicorn main:app --reload
     ```
   - Acesse a API: [http://127.0.0.1:8000](http://127.0.0.1:8000)  
     Documentação Swagger: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

3. **Frontend:**
   - Abra o arquivo `frontend/index.html` diretamente no navegador.

   - **Ou use o Live Server (VS Code):**
     Clique com o botão direito em `index.html` > "Open with Live Server"  
     Geralmente será iniciado em [http://127.0.0.1:5500](http://127.0.0.1:5500)

---

## 📁 Estrutura do Projeto

```
sistema-investimentos/
├── backend/
│   └── main.py
├── frontend/
│   └── index.html
├── requirements.txt
└── README.md
```

---

## 🧑‍💻 Autor

Desenvolvido por [Pablo Augusto](https://github.com/pabloaugussto) 💙
