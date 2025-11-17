# ⚡ Quick Start - StudyBuddy Backend

Guia rápido para colocar o backend em funcionamento em 5 minutos.

---

## 🚀 Passo 1: Preparar o Ambiente

```bash
# 1. Navegar para o diretório do projeto
cd studybuddy_backend

# 2. Criar ambiente virtual
python -m venv venv

# 3. Ativar ambiente virtual
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# 4. Instalar dependências
pip install -r requirements.txt
```

---

## 🔧 Passo 2: Configurar o Banco de Dados

```bash
# 1. Copiar arquivo de exemplo
cp .env.example .env

# 2. Editar .env com suas credenciais PostgreSQL
# Abra o arquivo .env e atualize:
# DATABASE_URL=postgresql://seu_usuario:sua_senha@localhost:5432/studybuddy_db
```

**No PostgreSQL (psql):**

```sql
-- Criar banco de dados
CREATE DATABASE studybuddy_db;

-- Conectar ao banco
\c studybuddy_db

-- Executar o script SQL (caminho relativo)
\i ../studybuddy_schema.sql
```

---

## ▶️ Passo 3: Executar a API

```bash
python -m uvicorn app.main:app --reload
```

**Saída esperada:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

---

## 📚 Passo 4: Testar a API

Abra seu navegador e acesse:

- **Documentação Interativa**: http://localhost:8000/docs
- **API Root**: http://localhost:8000/
- **Health Check**: http://localhost:8000/health

---

## 🧪 Exemplo de Requisição (cURL)

### Registrar um Usuário

```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "seu_usuario",
    "email": "seu_email@example.com",
    "password": "sua_senha"
  }'
```

**Resposta esperada:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "seu_usuario",
    "email": "seu_email@example.com",
    "created_at": "2025-11-16T21:00:00",
    "updated_at": "2025-11-16T21:00:00"
  }
}
```

### Criar um Desafio (Requer Token)

```bash
curl -X POST "http://localhost:8000/api/challenges" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -d '{
    "name": "Desafio de Química",
    "subject": "Química Orgânica",
    "description": "Estudar grupos funcionais",
    "daily_time": 60,
    "duration": 30
  }'
```

---

## 🔑 Variáveis de Ambiente Importantes

```env
# Banco de Dados
DATABASE_URL=postgresql://usuario:senha@localhost:5432/studybuddy_db

# Segurança (MUDE EM PRODUÇÃO!)
SECRET_KEY=sua-chave-secreta-aqui

# Configuração
DEBUG=True
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000", "http://localhost:5173"]
```

---

## 📋 Checklist de Configuração

- [ ] Python 3.8+ instalado
- [ ] PostgreSQL instalado e em execução
- [ ] Banco de dados `studybuddy_db` criado
- [ ] Tabelas criadas (script SQL executado)
- [ ] Arquivo `.env` configurado
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] API iniciada com sucesso
- [ ] Documentação acessível em `/docs`

---

## 🐛 Solução Rápida de Problemas

| Problema | Solução |
| :--- | :--- |
| `ModuleNotFoundError: No module named 'fastapi'` | Execute `pip install -r requirements.txt` |
| `could not connect to server` | Verifique se PostgreSQL está em execução |
| `password authentication failed` | Verifique a senha em `DATABASE_URL` |
| `database does not exist` | Execute `CREATE DATABASE studybuddy_db;` no psql |
| `relation does not exist` | Execute o script SQL para criar as tabelas |
| `CORS error` | Verifique se a origem do frontend está em `CORS_ORIGINS` |

---

## 📖 Documentação Completa

Para informações mais detalhadas, consulte:

- **README.md** - Documentação principal
- **CONEXAO_BANCO_DADOS.md** - Guia de conexão com PostgreSQL
- **ESTRUTURA_PROJETO.md** - Estrutura completa do projeto

---

## 🎯 Próximos Passos

1. Explorar a documentação interativa em `/docs`
2. Testar os endpoints usando o Swagger UI
3. Integrar com o frontend
4. Adicionar mais funcionalidades conforme necessário

---

**Pronto para começar? Boa sorte! 🚀**
