# 🔗 Guia de Conexão com o Banco de Dados PostgreSQL

Este documento descreve como configurar e conectar o backend StudyBuddy ao banco de dados PostgreSQL.

---

## 📋 Pré-requisitos

1. **PostgreSQL instalado** (versão 12 ou superior)
2. **Banco de dados `studybuddy_db` criado**
3. **Tabelas criadas** usando o script SQL fornecido

---

## 🚀 Passo 1: Criar o Banco de Dados

Se você ainda não criou o banco de dados, abra o `psql` e execute:

```sql
CREATE DATABASE studybuddy_db;
```

---

## 🚀 Passo 2: Criar as Tabelas

Conecte-se ao banco de dados e execute o script SQL:

```bash
# No terminal
psql -U postgres -d studybuddy_db -f /caminho/para/studybuddy_schema.sql
```

Ou, dentro do `psql`:

```sql
\c studybuddy_db
\i /caminho/para/studybuddy_schema.sql
```

---

## 🚀 Passo 3: Configurar a Variável de Ambiente

Crie um arquivo `.env` na raiz do projeto `studybuddy_backend/` com a seguinte configuração:

```env
# Configuração do Banco de Dados PostgreSQL
DATABASE_URL=postgresql://seu_usuario:sua_senha@localhost:5432/studybuddy_db

# Exemplo com usuário padrão do PostgreSQL
DATABASE_URL=postgresql://postgres:sua_senha@localhost:5432/studybuddy_db

# Se você não definiu uma senha para o usuário postgres
DATABASE_URL=postgresql://postgres@localhost:5432/studybuddy_db
```

### Explicação da URL de Conexão

```
postgresql://[usuario]:[senha]@[host]:[porta]/[banco_de_dados]
```

- **usuario**: Nome do usuário PostgreSQL (padrão: `postgres`)
- **senha**: Senha do usuário
- **host**: Endereço do servidor (padrão: `localhost`)
- **porta**: Porta do PostgreSQL (padrão: `5432`)
- **banco_de_dados**: Nome do banco de dados (`studybuddy_db`)

---

## 🔐 Passo 4: Configurar Outras Variáveis de Ambiente

Além da `DATABASE_URL`, configure as outras variáveis necessárias no arquivo `.env`:

```env
# Configuração do Banco de Dados
DATABASE_URL=postgresql://postgres:sua_senha@localhost:5432/studybuddy_db

# Configuração de Segurança
SECRET_KEY=sua-chave-secreta-muito-segura-aqui-mude-em-producao
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Configuração da API
DEBUG=True
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000", "http://localhost:5173"]
```

---

## 🧪 Passo 5: Testar a Conexão

Execute a API para verificar se a conexão com o banco de dados está funcionando:

```bash
python -m uvicorn app.main:app --reload
```

Se a API iniciar sem erros, a conexão está funcionando corretamente.

---

## 📊 Verificar a Conexão Manualmente

Para verificar se as tabelas foram criadas corretamente, conecte-se ao banco de dados:

```bash
psql -U postgres -d studybuddy_db
```

E execute:

```sql
-- Listar todas as tabelas
\dt

-- Verificar a estrutura de uma tabela
\d "User"
```

---

## 🔧 Solução de Problemas

### Erro: "could not translate host name"
**Causa**: O PostgreSQL não está em execução ou o host está incorreto.

**Solução**:
1. Verifique se o PostgreSQL está em execução
2. Verifique se o host está correto (geralmente `localhost` ou `127.0.0.1`)

### Erro: "password authentication failed"
**Causa**: A senha está incorreta.

**Solução**:
1. Verifique a senha do usuário PostgreSQL
2. Se você não lembra da senha, redefina-a:
   ```sql
   ALTER USER postgres WITH PASSWORD 'nova_senha';
   ```

### Erro: "database does not exist"
**Causa**: O banco de dados não foi criado.

**Solução**:
1. Crie o banco de dados:
   ```sql
   CREATE DATABASE studybuddy_db;
   ```

### Erro: "relation does not exist"
**Causa**: As tabelas não foram criadas.

**Solução**:
1. Execute o script SQL para criar as tabelas:
   ```bash
   psql -U postgres -d studybuddy_db -f studybuddy_schema.sql
   ```

---

## 🔄 Fluxo de Conexão

```
┌─────────────────────────────────────────┐
│     Aplicação FastAPI (app/main.py)     │
└──────────────────┬──────────────────────┘
                   │
                   ├─→ app/database.py
                   │   (Cria a engine SQLAlchemy)
                   │
                   ├─→ app/config.py
                   │   (Lê DATABASE_URL do .env)
                   │
                   └─→ PostgreSQL
                       (Banco de dados)
```

### Como Funciona

1. **app/config.py** lê a variável `DATABASE_URL` do arquivo `.env`
2. **app/database.py** cria uma engine SQLAlchemy usando essa URL
3. **Cada rota** usa `SessionLocal()` para obter uma sessão do banco de dados
4. **As queries** são executadas através da sessão ORM

---

## 📝 Exemplo de Query

Aqui está um exemplo de como a API interage com o banco de dados:

```python
# Em app/routes/auth.py
from app.database import get_db
from app.models import User

@router.post("/login")
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    # db é uma sessão do banco de dados
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    
    return {"message": "Login bem-sucedido"}
```

---

## 🔒 Segurança em Produção

Quando colocar a API em produção:

1. **Não exponha credenciais**: Nunca commite o arquivo `.env` com dados sensíveis
2. **Use variáveis de ambiente**: Configure as variáveis no servidor/plataforma de hospedagem
3. **Altere a SECRET_KEY**: Use uma chave aleatória e segura
4. **Use SSL/TLS**: Conecte-se ao PostgreSQL com SSL em produção
5. **Restrinja o acesso**: Configure o firewall para aceitar conexões apenas de IPs confiáveis

---

## 📚 Referências

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [FastAPI Database Documentation](https://fastapi.tiangolo.com/tutorial/sql-databases/)

---

**Desenvolvido com ❤️ para otimizar seus estudos!**
