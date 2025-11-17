# StudyBuddy Backend API

Backend da aplicação StudyBuddy desenvolvido com **Python**, **FastAPI** e **PostgreSQL**.

## 📋 Pré-requisitos

Antes de começar, certifique-se de que você tem instalado:

- **Python 3.8+**
- **PostgreSQL 12+**
- **pip** (gerenciador de pacotes do Python)

## 🚀 Instalação e Configuração

### 1. Clonar ou Baixar o Projeto

```bash
cd studybuddy_backend
```

### 2. Criar um Ambiente Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env` e configure as variáveis:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas configurações:

```env
# Configuração do Banco de Dados PostgreSQL
DATABASE_URL=postgresql://seu_usuario:sua_senha@localhost:5432/studybuddy_db

# Configuração de Segurança
SECRET_KEY=sua-chave-secreta-aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Configuração da API
DEBUG=True
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000", "http://localhost:5173"]
```

### 5. Criar o Banco de Dados

Se você ainda não criou o banco de dados PostgreSQL, execute:

```bash
# No psql
CREATE DATABASE studybuddy_db;
```

Depois, execute o script SQL fornecido (`studybuddy_schema.sql`) para criar as tabelas:

```bash
# No psql, conectado ao banco studybuddy_db
\i /caminho/para/studybuddy_schema.sql
```

## 🏃 Executar a API

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

A API estará disponível em: **http://localhost:8000**

### Acessar a Documentação Interativa

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📚 Estrutura do Projeto

```
studybuddy_backend/
├── app/
│   ├── models/              # Modelos ORM (SQLAlchemy)
│   │   ├── user.py
│   │   ├── session.py
│   │   ├── challenge.py
│   │   ├── summary.py
│   │   ├── question.py
│   │   ├── test_result.py
│   │   └── __init__.py
│   ├── routes/              # Rotas da API
│   │   ├── auth.py          # Autenticação (login/registro)
│   │   ├── challenges.py    # Gerenciamento de desafios
│   │   ├── summaries.py     # Resumos de estudo
│   │   ├── questions.py     # Perguntas de avaliação
│   │   ├── results.py       # Resultados de testes
│   │   ├── dashboard.py     # Dashboard e calendário
│   │   └── __init__.py
│   ├── schemas/             # Schemas Pydantic (validação)
│   │   ├── user.py
│   │   ├── challenge.py
│   │   ├── summary.py
│   │   ├── question.py
│   │   ├── test_result.py
│   │   └── __init__.py
│   ├── utils/               # Utilitários
│   │   ├── security.py      # Hash de senha e JWT
│   │   ├── auth.py          # Autenticação e dependências
│   │   └── __init__.py
│   ├── config.py            # Configurações da aplicação
│   ├── database.py          # Conexão com o banco de dados
│   ├── main.py              # Aplicação FastAPI principal
│   └── __init__.py
├── tests/                   # Testes unitários
├── .env.example             # Exemplo de variáveis de ambiente
├── requirements.txt         # Dependências do projeto
└── README.md               # Este arquivo
```

## 🔐 Autenticação

A API utiliza **JWT (JSON Web Tokens)** para autenticação. Todos os *endpoints* protegidos requerem um token de acesso no header `Authorization`:

```
Authorization: Bearer <seu_token_jwt>
```

### Fluxo de Autenticação

1. **Registrar um novo usuário**: `POST /api/auth/register`
2. **Fazer login**: `POST /api/auth/login`
3. **Usar o token retornado** em todas as requisições protegidas

## 📡 Endpoints Principais

### Autenticação
- `POST /api/auth/register` - Registrar novo usuário
- `POST /api/auth/login` - Fazer login

### Desafios
- `POST /api/challenges` - Criar novo desafio
- `GET /api/challenges` - Listar desafios do usuário
- `GET /api/challenges/{id}` - Obter detalhes de um desafio
- `PUT /api/challenges/{id}` - Atualizar desafio
- `DELETE /api/challenges/{id}` - Deletar desafio

### Resumos
- `POST /api/summaries` - Criar novo resumo
- `GET /api/summaries` - Listar resumos do usuário
- `GET /api/summaries/{id}` - Obter detalhes de um resumo
- `DELETE /api/summaries/{id}` - Deletar resumo

### Perguntas
- `POST /api/questions` - Criar nova pergunta
- `GET /api/questions/challenge/{challenge_id}` - Listar perguntas de um desafio
- `GET /api/questions/{id}` - Obter detalhes de uma pergunta
- `DELETE /api/questions/{id}` - Deletar pergunta

### Resultados
- `POST /api/results/submit` - Submeter respostas e calcular resultado
- `GET /api/results/{id}` - Obter detalhes de um resultado
- `GET /api/results/challenge/{challenge_id}` - Listar resultados de um desafio
- `GET /api/results` - Listar todos os resultados do usuário

### Dashboard
- `GET /api/streak-days` - Obter datas de estudo (para calendário)
- `GET /api/day/{date}` - Obter dados de um dia específico
- `GET /api/dashboard/overview` - Obter visão geral do dashboard

## 🔗 Integração com o Frontend

O frontend deve fazer requisições HTTP para os *endpoints* da API. Exemplo com `fetch`:

```javascript
// Registrar novo usuário
const response = await fetch('http://localhost:8000/api/auth/register', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    username: 'seu_usuario',
    email: 'seu_email@example.com',
    password: 'sua_senha'
  })
});

const data = await response.json();
const token = data.access_token;

// Usar o token em requisições protegidas
const challengesResponse = await fetch('http://localhost:8000/api/challenges', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});
```

## 🛠️ Desenvolvimento

### Adicionar Novas Rotas

1. Criar um novo arquivo em `app/routes/`
2. Definir as rotas usando FastAPI
3. Importar e incluir o router em `app/main.py`

### Adicionar Novos Modelos

1. Criar um novo arquivo em `app/models/`
2. Definir a classe do modelo herdando de `Base`
3. Importar em `app/models/__init__.py`

### Adicionar Novos Schemas

1. Criar um novo arquivo em `app/schemas/`
2. Definir as classes Pydantic para validação
3. Importar em `app/schemas/__init__.py`

## 🧪 Testes

Para executar os testes (quando implementados):

```bash
pytest tests/
```

## 📝 Notas Importantes

- **Segurança**: Altere a `SECRET_KEY` em produção para uma chave aleatória e segura.
- **CORS**: Configure as origens permitidas em `CORS_ORIGINS` de acordo com seu frontend.
- **Banco de Dados**: Certifique-se de que o PostgreSQL está em execução antes de iniciar a API.
- **Variáveis de Ambiente**: Nunca commite o arquivo `.env` com dados sensíveis no repositório.

## 🐛 Solução de Problemas

### Erro: "could not connect to server"
- Verifique se o PostgreSQL está em execução
- Verifique as credenciais em `DATABASE_URL`

### Erro: "table does not exist"
- Execute o script SQL para criar as tabelas
- Verifique se o banco de dados foi criado corretamente

### Erro: "CORS error"
- Adicione a origem do seu frontend em `CORS_ORIGINS` no arquivo `.env`

## 📞 Suporte

Para dúvidas ou problemas, consulte a documentação do FastAPI:
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

## 📄 Licença

Projeto educacional - Use livremente para estudos e projetos pessoais.

---

**Desenvolvido com ❤️ para otimizar seus estudos!**
