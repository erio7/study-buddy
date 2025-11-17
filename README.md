# 📚 StudyBuddy - Gamificação de Estudo

> Um aplicativo de gamificação para incentivar e acompanhar a rotina de estudos dos usuários através de desafios, pontos e progresso.

---

## 📖 Visão Geral

O **StudyBuddy** é uma plataforma completa de gamificação para estudos que permite aos usuários:

- 🎯 **Criar e Gerenciar Desafios** de estudo com metas diárias e mensais
- 📝 **Registrar Progresso Diário** com resumos, tempo de estudo e fotos
- 🤖 **Validar Conhecimento** através de perguntas geradas por IA
- 📊 **Acompanhar Progresso** através de dashboards e calendários
- 🔔 **Receber Notificações** para manter a motivação

---

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.13** - Linguagem de programação
- **FastAPI 0.104.1** - Framework web moderno e rápido
- **SQLAlchemy 2.0.23** - ORM para banco de dados
- **Uvicorn 0.24.0** - Servidor ASGI
- **JWT (python-jose)** - Autenticação segura
- **Bcrypt** - Hash de senhas

### Banco de Dados
- **PostgreSQL** - Sistema de banco de dados relacional robusto
- **psycopg2** - Driver PostgreSQL para Python

### Frontend
- **HTML5** - Estrutura semântica
- **CSS3** - Styling responsivo
- **JavaScript Vanilla** - Interatividade e lógica do cliente

### Ferramentas de Desenvolvimento
- **Postman** - Testes de API
- **Git** - Controle de versão

---

## 📁 Estrutura do Projeto

```
study-buddy/
│
├── backend/                          # Aplicação FastAPI (API REST)
│   ├── app/
│   │   ├── models/                  # Modelos ORM (SQLAlchemy)
│   │   │   ├── __init__.py
│   │   │   ├── user.py              # Modelo de Usuário
│   │   │   ├── session.py           # Modelo de Sessão/Token
│   │   │   ├── challenge.py         # Modelo de Desafio
│   │   │   ├── summary.py           # Modelo de Resumo Diário
│   │   │   ├── question.py          # Modelo de Pergunta
│   │   │   └── test_result.py       # Modelo de Resultado de Teste
│   │   │
│   │   ├── routes/                  # Rotas da API (endpoints)
│   │   │   ├── __init__.py
│   │   │   ├── auth.py              # Autenticação (registro, login)
│   │   │   ├── challenges.py        # CRUD de Desafios
│   │   │   ├── summaries.py         # CRUD de Resumos
│   │   │   ├── questions.py         # CRUD de Perguntas
│   │   │   ├── results.py           # Resultados de Testes
│   │   │   └── dashboard.py         # Dashboard e Calendário
│   │   │
│   │   ├── schemas/                 # Schemas Pydantic (validação)
│   │   │   ├── __init__.py
│   │   │   ├── user.py              # Schemas de Usuário
│   │   │   ├── challenge.py         # Schemas de Desafio
│   │   │   ├── summary.py           # Schemas de Resumo
│   │   │   ├── question.py          # Schemas de Pergunta
│   │   │   └── test_result.py       # Schemas de Resultado
│   │   │
│   │   ├── utils/                   # Utilitários
│   │   │   ├── __init__.py
│   │   │   ├── security.py          # Hash de senha, JWT
│   │   │   └── auth.py              # Dependências de autenticação
│   │   │
│   │   ├── __init__.py
│   │   ├── main.py                  # Aplicação principal
│   │   ├── config.py                # Configurações
│   │   └── database.py              # Conexão com BD
│   │
│   ├── tests/                        # Testes unitários (futuro)
│   ├── venv/                         # Ambiente virtual Python
│   ├── .env.example                  # Exemplo de variáveis de ambiente
│   ├── requirements.txt              # Dependências Python
│   └── README.md                     # Documentação do backend
│
├── frontend/                         # Aplicação HTML/CSS/JS
│   ├── js/
│   │   ├── api.js                   # Cliente API (integração com backend)
│   │   ├── app.js                   # Lógica principal da aplicação
│   │   └── calendar.js              # Lógica do calendário
│   │
│   ├── css/
│   │   └── style.css                # Estilos globais
│   │
│   ├── index.html                   # Página inicial
│   ├── login.html                   # Página de login
│   ├── register.html                # Página de registro
│   ├── home.html                    # Dashboard principal
│   ├── create-challenge.html        # Criar novo desafio
│   ├── challenge-detail.html        # Detalhes do desafio
│   ├── day-view.html                # Registrar dia de estudo
│   ├── questions.html               # Perguntas de avaliação
│   ├── results.html                 # Resultados dos testes
│   ├── profile.html                 # Perfil do usuário
│   ├── resumo.html                  # Resumo de progresso
│   └── README.md                    # Documentação do frontend
│
├── database/
│   └── studybuddy_schema.sql        # Script SQL para criar tabelas
│
├── docs/                             # Documentação adicional
│   ├── GUIA_INSTALACAO_E_ESTRUTURA.md
│   ├── GUIA_TESTES_ENDPOINTS.md
│   ├── GUIA_POSTMAN.md
│   └── GUIA_INTEGRACAO_FRONTEND_BACKEND.md
│
├── .gitignore
├── README.md                         # Este arquivo
└── LICENSE

```

---

## 🚀 Início Rápido

### Pré-requisitos

Certifique-se de ter instalado:

- **Python 3.13+** - [Download](https://www.python.org/downloads/)
- **PostgreSQL 12+** - [Download](https://www.postgresql.org/download/)
- **Git** - [Download](https://git-scm.com/)
- **Postman** (opcional, para testes) - [Download](https://www.postman.com/downloads/)

### 1️⃣ Clonar o Repositório

```bash
git clone https://github.com/erio7/study-buddy.git
cd study-buddy
```

### 2️⃣ Configurar o Banco de Dados

#### 2.1 Criar o Banco de Dados

Abra o **psql** (PostgreSQL CLI):

```bash
psql -U postgres
```

Digite a senha do PostgreSQL quando solicitado.

#### 2.2 Criar o Banco

```sql
CREATE DATABASE studybuddy_db;
```

#### 2.3 Conectar ao Banco

```sql
\c studybuddy_db
```

#### 2.4 Executar o Script SQL

```sql
\i C:/Users/seu_usuario/study-buddy/database/studybuddy_schema.sql
```

**Ou no Windows (com barras normais)**:

```sql
\i C:/Users/seu_usuario/study-buddy/database/studybuddy_schema.sql
```

#### 2.5 Verificar as Tabelas

```sql
\dt
```

Você deve ver as tabelas criadas. Depois, saia:

```sql
\q
```

### 3️⃣ Configurar o Backend

#### 3.1 Navegar para a Pasta Backend

```bash
cd backend
```

#### 3.2 Criar Ambiente Virtual

```bash
python -m venv venv
```

#### 3.3 Ativar o Ambiente Virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

#### 3.4 Instalar Dependências

```bash
pip install -r requirements.txt
```

#### 3.5 Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz da pasta `backend`:

```bash
copy .env.example .env
```

Abra o arquivo `.env` e configure:

```env
# Banco de Dados PostgreSQL
DATABASE_URL=postgresql://postgres:sua_senha@localhost:5432/studybuddy_db

# Segurança
SECRET_KEY=sua-chave-secreta-muito-segura-aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API
DEBUG=True
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000", "http://localhost:5173", "http://localhost:8001"]
```

**Para gerar uma SECRET_KEY segura:**

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### 3.6 Executar o Backend

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Saída esperada:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

✅ **Backend rodando em**: http://localhost:8000

### 4️⃣ Configurar o Frontend

#### 4.1 Abrir Nova Aba do Terminal

Mantenha o backend rodando e abra um novo Command Prompt.

#### 4.2 Navegar para a Pasta Frontend

```bash
cd frontend
```

#### 4.3 Iniciar Servidor Local

```bash
python -m http.server 8001
```

**Saída esperada:**
```
Serving HTTP on 0.0.0.0 port 8001 (http://0.0.0.0:8001/) ...
```

✅ **Frontend rodando em**: http://localhost:8001

### 5️⃣ Acessar a Aplicação

Abra seu navegador e acesse:

- **Frontend**: http://localhost:8001
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API ReDoc**: http://localhost:8000/redoc

---

## 📚 Como Usar

### 1. Registrar uma Conta

1. Acesse http://localhost:8001/register.html
2. Preencha os dados (username, email, senha)
3. Clique em "Registrar"

### 2. Fazer Login

1. Acesse http://localhost:8001/login.html
2. Use as credenciais que você registrou
3. Clique em "Fazer Login"

### 3. Criar um Desafio

1. Após login, clique em "+ Novo Desafio"
2. Preencha os dados do desafio
3. Clique em "Criar Desafio"

### 4. Registrar um Dia de Estudo

1. Na página inicial, clique em "Registrar" em um desafio
2. Preencha o formulário (data, horas, dificuldade, resumo)
3. Clique em "Registrar Resumo"

### 5. Acompanhar Progresso

1. Acesse o Dashboard para ver:
   - Desafios ativos
   - Horas de estudo
   - Dias com estudo (streak)
   - Progresso geral

---

## 🧪 Testando a API

### Opção 1: Swagger UI (Recomendado)

1. Acesse http://localhost:8000/docs
2. Clique em cada endpoint
3. Clique em "Try it out"
4. Preencha os dados
5. Clique em "Execute"

### Opção 2: Postman

1. Descarregue a collection: `StudyBuddy_API.postman_collection.json`
2. Importe no Postman
3. Configure a variável `base_url` para `http://localhost:8000`
4. Teste os endpoints

### Opção 3: cURL

```bash
# Registrar
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"teste","email":"teste@example.com","password":"abc123"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"teste@example.com","password":"abc123"}'
```

---

## 📋 Endpoints Principais

### Autenticação
| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| POST | `/api/auth/register` | Registrar novo usuário |
| POST | `/api/auth/login` | Fazer login |

### Desafios
| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| POST | `/api/challenges` | Criar novo desafio |
| GET | `/api/challenges` | Listar desafios do usuário |
| GET | `/api/challenges/{id}` | Obter detalhes de um desafio |
| PUT | `/api/challenges/{id}` | Atualizar desafio |
| DELETE | `/api/challenges/{id}` | Deletar desafio |

### Resumos
| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| POST | `/api/summaries` | Criar novo resumo |
| GET | `/api/summaries` | Listar resumos |
| GET | `/api/summaries/{id}` | Obter resumo específico |
| GET | `/api/summaries/by-date/{date}` | Obter resumos de uma data |
| PUT | `/api/summaries/{id}` | Atualizar resumo |
| DELETE | `/api/summaries/{id}` | Deletar resumo |

### Dashboard
| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| GET | `/api/streak-days` | Obter dias com estudo |
| GET | `/api/day/{date}` | Obter dados de um dia |
| GET | `/api/dashboard/overview` | Obter visão geral |

**Para mais endpoints, consulte a documentação em `/api/docs`**

---

## 🔐 Segurança

### Autenticação JWT

- Tokens JWT são gerados após login
- Tokens expiram em 30 minutos
- Senhas são criptografadas com bcrypt
- Máximo de 72 caracteres por senha

### Variáveis de Ambiente

Nunca commite o arquivo `.env` com credenciais reais. Use `.env.example` como template.

### CORS

O backend está configurado para aceitar requisições do frontend em `http://localhost:8001`.

---

## 🐛 Solução de Problemas

### Erro: "Connection refused"
- ✅ Verifique se o PostgreSQL está rodando
- ✅ Verifique se o backend está rodando em `http://localhost:8000`

### Erro: "Database does not exist"
- ✅ Verifique se você criou o banco de dados
- ✅ Verifique se o `DATABASE_URL` está correto no `.env`

### Erro: "password cannot be longer than 72 bytes"
- ✅ Use uma senha com menos de 72 caracteres

### Erro: "401 Unauthorized"
- ✅ Verifique se o token JWT é válido
- ✅ Faça login novamente para obter um novo token

### Erro: "CORS error"
- ✅ Verifique se o frontend está em `http://localhost:8001`
- ✅ Verifique a configuração de `CORS_ORIGINS` no `.env`

---

## 📚 Documentação Adicional

- [Guia de Instalação e Estrutura](./docs/GUIA_INSTALACAO_E_ESTRUTURA.md)
- [Guia de Testes de Endpoints](./docs/GUIA_TESTES_ENDPOINTS.md)
- [Guia do Postman](./docs/GUIA_POSTMAN.md)
- [Guia de Integração Frontend-Backend](./docs/GUIA_INTEGRACAO_FRONTEND_BACKEND.md)

---

## 🤝 Como Contribuir

Agradecemos a todos que desejam contribuir! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/sua-feature`)
3. Commit suas mudanças (`git commit -m 'feat: Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/sua-feature`)
5. Abra um Pull Request

---



## 📄 Licença

Este projeto está sob a licença **erioBD**. Veja o arquivo `LICENSE` para mais detalhes.

---

## 👥 Autores

- **Eric Amorim** - Desenvolvedor Principal

---

## 📞 Suporte

Para dúvidas, sugestões ou relatórios de bugs, abra uma **Issue** no repositório ou entre em contato através do email.

---

## 🔗 Links Úteis

- [Figma - Protótipo](https://www.figma.com/board/bJzkc3zRmqlneONrVM8XMm/MOSCOW---STUDYBUDDY?node-id=0-1&t=E7q75GPXAZJeUcrf-1)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)

---

**Desenvolvido com ❤️ por Eric Amorim**

Last Updated: Novembro 2024
