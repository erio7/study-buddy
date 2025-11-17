# 📁 Estrutura Completa do Projeto StudyBuddy Backend

Este documento descreve a estrutura de diretórios e arquivos do backend StudyBuddy.

---

## 🏗️ Árvore de Diretórios

```
studybuddy_backend/
│
├── app/                          # Pacote principal da aplicação
│   ├── __init__.py              # Inicialização do pacote
│   ├── main.py                  # Aplicação FastAPI principal
│   ├── config.py                # Configurações da aplicação
│   ├── database.py              # Conexão e sessão do banco de dados
│   │
│   ├── models/                  # Modelos ORM (SQLAlchemy)
│   │   ├── __init__.py
│   │   ├── user.py              # Modelo de Usuário
│   │   ├── session.py           # Modelo de Sessão (Autenticação)
│   │   ├── challenge.py         # Modelo de Desafio
│   │   ├── summary.py           # Modelo de Resumo (Registro Diário)
│   │   ├── question.py          # Modelo de Pergunta
│   │   └── test_result.py       # Modelos de Resultado e Resposta
│   │
│   ├── routes/                  # Rotas da API
│   │   ├── __init__.py
│   │   ├── auth.py              # Rotas de Autenticação (Login/Registro)
│   │   ├── challenges.py        # Rotas de Gerenciamento de Desafios
│   │   ├── summaries.py         # Rotas de Resumos de Estudo
│   │   ├── questions.py         # Rotas de Perguntas
│   │   ├── results.py           # Rotas de Resultados de Testes
│   │   └── dashboard.py         # Rotas de Dashboard e Calendário
│   │
│   ├── schemas/                 # Schemas Pydantic (Validação de Dados)
│   │   ├── __init__.py
│   │   ├── user.py              # Schemas de Usuário
│   │   ├── challenge.py         # Schemas de Desafio
│   │   ├── summary.py           # Schemas de Resumo
│   │   ├── question.py          # Schemas de Pergunta
│   │   └── test_result.py       # Schemas de Resultado e Resposta
│   │
│   └── utils/                   # Utilitários e Funções Auxiliares
│       ├── __init__.py
│       ├── security.py          # Hash de Senha e JWT
│       └── auth.py              # Autenticação e Dependências
│
├── tests/                       # Testes Unitários e de Integração
│   └── (testes a implementar)
│
├── .env.example                 # Exemplo de Variáveis de Ambiente
├── requirements.txt             # Dependências do Projeto
├── README.md                    # Documentação Principal
├── CONEXAO_BANCO_DADOS.md      # Guia de Conexão com PostgreSQL
└── ESTRUTURA_PROJETO.md        # Este arquivo
```

---

## 📄 Descrição dos Arquivos Principais

### `app/main.py`
**Propósito**: Arquivo principal da aplicação FastAPI.

**Responsabilidades**:
- Criar a instância da aplicação FastAPI
- Configurar middleware CORS
- Incluir todas as rotas
- Definir rotas raiz (`/` e `/health`)

**Exemplo**:
```python
from fastapi import FastAPI
from app.routes import auth_router, challenges_router, ...

app = FastAPI(title="StudyBuddy API")
app.include_router(auth_router)
```

---

### `app/config.py`
**Propósito**: Centralizar todas as configurações da aplicação.

**Responsabilidades**:
- Ler variáveis de ambiente do arquivo `.env`
- Definir valores padrão para configurações
- Fornecer um objeto `settings` global

**Exemplo**:
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    CORS_ORIGINS: List[str]

settings = Settings()
```

---

### `app/database.py`
**Propósito**: Gerenciar a conexão com o banco de dados PostgreSQL.

**Responsabilidades**:
- Criar a engine SQLAlchemy
- Criar a factory de sessões
- Fornecer a dependência `get_db()` para as rotas

**Exemplo**:
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

## 🗂️ Modelos (app/models/)

Os modelos definem a estrutura das tabelas do banco de dados usando SQLAlchemy ORM.

### `user.py`
Representa um usuário da aplicação.

**Campos**:
- `id` (PK)
- `username` (UNIQUE)
- `email` (UNIQUE)
- `password_hash`
- `created_at`
- `updated_at`

### `session.py`
Armazena tokens de autenticação dos usuários.

**Campos**:
- `id` (PK)
- `user_id` (FK)
- `token` (UNIQUE)
- `expires_at`
- `ip_address`
- `user_agent`
- `created_at`

### `challenge.py`
Representa um desafio de estudo criado pelo usuário.

**Campos**:
- `id` (PK)
- `user_id` (FK)
- `name`
- `subject`
- `description`
- `daily_time` (minutos)
- `duration` (dias)
- `photo_url`
- `created_at`
- `updated_at`

### `summary.py`
Armazena resumos/registros diários de estudo.

**Campos**:
- `id` (PK)
- `user_id` (FK)
- `challenge_id` (FK, opcional)
- `study_date`
- `study_time` (minutos)
- `difficulty` (ENUM: Fácil, Médio, Difícil)
- `summary_text`
- `photo_url`
- `created_at`
- `updated_at`

**Relacionamento**:
- Um `Summary` pode ter múltiplos `SummaryObjective`

### `question.py`
Representa uma pergunta de múltipla escolha.

**Campos**:
- `id` (PK)
- `challenge_id` (FK)
- `text`
- `options` (JSON)
- `correct_answer` (a, b, c, d, e)
- `created_at`

### `test_result.py`
Armazena os resultados de testes realizados pelo usuário.

**Campos**:
- `id` (PK)
- `user_id` (FK)
- `challenge_id` (FK)
- `score` (0-100)
- `correct_count`
- `total_count`
- `time_spent` (minutos)
- `created_at`

**Relacionamento**:
- Um `TestResult` pode ter múltiplos `Answer`

---

## 🛣️ Rotas (app/routes/)

As rotas definem os endpoints da API.

### `auth.py`
**Endpoints**:
- `POST /api/auth/register` - Registrar novo usuário
- `POST /api/auth/login` - Fazer login

### `challenges.py`
**Endpoints**:
- `POST /api/challenges` - Criar desafio
- `GET /api/challenges` - Listar desafios
- `GET /api/challenges/{id}` - Obter desafio
- `PUT /api/challenges/{id}` - Atualizar desafio
- `DELETE /api/challenges/{id}` - Deletar desafio

### `summaries.py`
**Endpoints**:
- `POST /api/summaries` - Criar resumo
- `GET /api/summaries` - Listar resumos
- `GET /api/summaries/{id}` - Obter resumo
- `DELETE /api/summaries/{id}` - Deletar resumo

### `questions.py`
**Endpoints**:
- `POST /api/questions` - Criar pergunta
- `GET /api/questions/challenge/{id}` - Listar perguntas de um desafio
- `GET /api/questions/{id}` - Obter pergunta
- `DELETE /api/questions/{id}` - Deletar pergunta

### `results.py`
**Endpoints**:
- `POST /api/results/submit` - Submeter respostas
- `GET /api/results/{id}` - Obter resultado
- `GET /api/results/challenge/{id}` - Listar resultados de um desafio
- `GET /api/results` - Listar todos os resultados

### `dashboard.py`
**Endpoints**:
- `GET /api/streak-days` - Obter datas de estudo (calendário)
- `GET /api/day/{date}` - Obter dados de um dia
- `GET /api/dashboard/overview` - Obter visão geral do dashboard

---

## 📋 Schemas (app/schemas/)

Os schemas definem a validação de dados de entrada/saída usando Pydantic.

### Exemplo de Schema

```python
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    
    class Config:
        from_attributes = True  # Permite converter modelos ORM
```

---

## 🔐 Utilitários (app/utils/)

### `security.py`
**Funções**:
- `hash_password(password)` - Cria hash da senha
- `verify_password(plain, hashed)` - Verifica senha
- `create_access_token(data)` - Cria token JWT
- `decode_token(token)` - Decodifica token JWT

### `auth.py`
**Funções**:
- `get_current_user(credentials, db)` - Dependência para obter usuário autenticado

---

## 🔄 Fluxo de Requisição

```
┌─────────────────────────────────────────┐
│        Cliente (Frontend)                │
└──────────────────┬──────────────────────┘
                   │
                   │ HTTP Request
                   ↓
┌─────────────────────────────────────────┐
│        FastAPI (app/main.py)             │
│  ├─ CORS Middleware                      │
│  └─ Rotas                                │
└──────────────────┬──────────────────────┘
                   │
                   ├─→ app/routes/*.py
                   │   (Processa a requisição)
                   │
                   ├─→ app/schemas/*.py
                   │   (Valida dados)
                   │
                   ├─→ app/utils/auth.py
                   │   (Autenticação)
                   │
                   ├─→ app/database.py
                   │   (Sessão do BD)
                   │
                   └─→ app/models/*.py
                       (Consultas ORM)
                       │
                       ↓
                   PostgreSQL
```

---

## 🚀 Como Adicionar uma Nova Funcionalidade

### Exemplo: Adicionar Rota de "Favoritos"

1. **Criar o Modelo** (`app/models/favorite.py`):
```python
from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base

class Favorite(Base):
    __tablename__ = "Favorite"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("User.id"))
    challenge_id = Column(Integer, ForeignKey("Challenge.id"))
```

2. **Criar o Schema** (`app/schemas/favorite.py`):
```python
from pydantic import BaseModel

class FavoriteCreate(BaseModel):
    challenge_id: int

class FavoriteResponse(BaseModel):
    id: int
    user_id: int
    challenge_id: int
```

3. **Criar as Rotas** (`app/routes/favorites.py`):
```python
from fastapi import APIRouter, Depends
from app.database import get_db
from app.models import Favorite
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/favorites", tags=["Favoritos"])

@router.post("", response_model=FavoriteResponse)
async def add_favorite(
    favorite_data: FavoriteCreate,
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    new_favorite = Favorite(
        user_id=current_user.id,
        challenge_id=favorite_data.challenge_id
    )
    db.add(new_favorite)
    db.commit()
    return new_favorite
```

4. **Incluir no Main** (`app/main.py`):
```python
from app.routes.favorites import router as favorites_router

app.include_router(favorites_router)
```

---

## 📊 Diagrama de Relacionamentos

```
User (1) ──────→ (N) Challenge
  │
  ├──→ (N) Session
  ├──→ (N) Summary
  └──→ (N) TestResult

Challenge (1) ──→ (N) Question
Challenge (1) ──→ (N) Summary
Challenge (1) ──→ (N) TestResult

Summary (1) ──→ (N) SummaryObjective

TestResult (1) ──→ (N) Answer
Question (1) ──→ (N) Answer
```

---

## 🔧 Configuração de Desenvolvimento

Para facilitar o desenvolvimento, use o modo `--reload` do Uvicorn:

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Isso reinicia automaticamente a API quando você faz mudanças no código.

---

## 📚 Referências

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

---

**Desenvolvido com ❤️ para otimizar seus estudos!**
