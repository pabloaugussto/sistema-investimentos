import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool # Para SQLite em memória com TestClient

# Importações do projeto
# Ajuste os caminhos se sua estrutura for diferente ou se 'main.py' e 'database.py'
# não estiverem diretamente na raiz do projeto em relação a 'tests/'
# Se 'main.py' está na raiz, e 'tests' é uma subpasta, os imports abaixo devem funcionar
# se você rodar pytest da raiz do projeto.
from main import app # aplicação FastAPI
from database import Base, get_db # Base e a dependência get_db
from models import Investimento as InvestimentoDB # modelo SQLAlchemy
from schemas import InvestimentoCreate, Investimento # schemas Pydantic

# --- Configuração do Banco de Dados de Teste ---
SQLALCHEMY_DATABASE_URL_TEST = "sqlite:///:memory:" # Banco de dados em memória

engine_test = create_engine(
    SQLALCHEMY_DATABASE_URL_TEST,
    connect_args={"check_same_thread": False}, # Necessário para SQLite
    poolclass=StaticPool, # Recomendado para SQLite em memória com TestClient
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

# --- Sobrescrever a Dependência get_db ---
# Esta função será usada no lugar da get_db original durante os testes
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Aplica a sobrescrita da dependência na aplicação FastAPI
# Isso garante que as rotas usem o banco de dados de teste
app.dependency_overrides[get_db] = override_get_db

# --- Fixture do Pytest para o Cliente de Teste e Banco de Dados ---
# Uma fixture é uma função que o pytest executa antes de cada teste que a solicita.
# Ela é usada para configurar o estado necessário para os testes.
@pytest.fixture(scope="function") # "function" scope: roda uma vez por função de teste
def client():
    # Cria as tabelas no banco de dados em memória ANTES de cada teste
    Base.metadata.create_all(bind=engine_test)
    
    # Cria o TestClient
    with TestClient(app) as c:
        yield c # Disponibiliza o cliente para o teste
    
    # Remove todas as tabelas do banco de dados em memória DEPOIS de cada teste
    Base.metadata.drop_all(bind=engine_test)

# --- Testes ---

def test_criar_investimento(client):
    """Testa a criação de um novo investimento."""
    dados_investimento = {
        "nome": "Tesouro Selic 2029",
        "tipo": "Renda Fixa",
        "valor": 1000.50,
        "data_investimento": "2024-05-29"
    }
    response = client.post("/api/v1/investimentos/", json=dados_investimento)
    assert response.status_code == 200, response.text # FastAPI retorna 200 para POST por padrão
    data = response.json()
    assert data["nome"] == dados_investimento["nome"]
    assert data["tipo"] == dados_investimento["tipo"]
    assert data["valor"] == dados_investimento["valor"]
    assert data["data_investimento"] == dados_investimento["data_investimento"]
    assert "id" in data

def test_listar_investimentos_vazio(client):
    """Testa a listagem quando não há investimentos."""
    response = client.get("/api/v1/investimentos/")
    assert response.status_code == 200, response.text
    assert response.json() == []

def test_listar_investimentos_com_dados(client):
    """Testa a listagem após criar um investimento."""
    dados_investimento = {
        "nome": "Ações XYZ",
        "tipo": "Renda Variável",
        "valor": 500.00,
        "data_investimento": "2024-01-15"
    }
    client.post("/api/v1/investimentos/", json=dados_investimento) # Cria um investimento

    response = client.get("/api/v1/investimentos/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) == 1
    assert data[0]["nome"] == dados_investimento["nome"]

def test_buscar_investimento_existente(client):
    """Testa buscar um investimento que existe."""
    dados_investimento = {
        "nome": "FII ABC",
        "tipo": "Fundo Imobiliário",
        "valor": 120.00,
        "data_investimento": "2023-11-10"
    }
    response_post = client.post("/api/v1/investimentos/", json=dados_investimento)
    investimento_id = response_post.json()["id"]

    response_get = client.get(f"/api/v1/investimentos/{investimento_id}")
    assert response_get.status_code == 200, response_get.text
    data = response_get.json()
    assert data["id"] == investimento_id
    assert data["nome"] == dados_investimento["nome"]

def test_buscar_investimento_nao_existente(client):
    """Testa buscar um investimento que não existe (deve retornar 404)."""
    response = client.get("/api/v1/investimentos/999") # ID que provavelmente não existe
    assert response.status_code == 404, response.text
    assert response.json()["detail"] == "Investimento não encontrado"

def test_atualizar_investimento(client):
    """Testa a atualização de um investimento existente."""
    dados_originais = {
        "nome": "CDB Banco Y",
        "tipo": "Renda Fixa",
        "valor": 2000.00,
        "data_investimento": "2024-02-01"
    }
    response_post = client.post("/api/v1/investimentos/", json=dados_originais)
    investimento_id = response_post.json()["id"]

    dados_atualizados = {
        "nome": "CDB Banco Y - Atualizado",
        "tipo": "Renda Fixa Premium",
        "valor": 2500.00,
        "data_investimento": "2024-02-05"
    }
    response_put = client.put(f"/api/v1/investimentos/{investimento_id}", json=dados_atualizados)
    assert response_put.status_code == 200, response_put.text
    data = response_put.json()
    assert data["nome"] == dados_atualizados["nome"]
    assert data["valor"] == dados_atualizados["valor"]
    assert data["data_investimento"] == dados_atualizados["data_investimento"]

def test_atualizar_investimento_nao_existente(client):
    """Testa atualizar um investimento que não existe (deve retornar 404)."""
    dados_atualizados = {
        "nome": "Não Existe",
        "tipo": "Nenhum",
        "valor": 0,
        "data_investimento": "2024-01-01"
    }
    response = client.put("/api/v1/investimentos/999", json=dados_atualizados)
    assert response.status_code == 404, response.text

def test_excluir_investimento(client):
    """Testa a exclusão de um investimento existente."""
    dados_investimento = {
        "nome": "Para Excluir",
        "tipo": "Temporário",
        "valor": 10.00,
        "data_investimento": "2024-03-03"
    }
    response_post = client.post("/api/v1/investimentos/", json=dados_investimento)
    investimento_id = response_post.json()["id"]

    response_delete = client.delete(f"/api/v1/investimentos/{investimento_id}")
    assert response_delete.status_code == 200, response_delete.text # Ou 204 se sua API retornar No Content
    assert response_delete.json()["message"] == "Investimento excluído com sucesso"  # Se sua API retorna uma mensagem
# Alterado para "message"
    # Verifica se foi realmente excluído
    response_get = client.get(f"/api/v1/investimentos/{investimento_id}")
    assert response_get.status_code == 404, response_get.text

def test_excluir_investimento_nao_existente(client):
    """Testa excluir um investimento que não existe (deve retornar 404)."""
    response = client.delete("/api/v1/investimentos/999")
    assert response.status_code == 404, response.text