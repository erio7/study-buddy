-- 1. Criação do Banco de Dados (Executar fora do psql ou com CREATE DATABASE)
-- CREATE DATABASE studybuddy_db;

-- 2. Conectar ao novo Banco de Dados (Executar dentro do psql)
-- \c studybuddy_db

-- 3. Criação dos Tipos ENUM
CREATE TYPE answer_option AS ENUM ('a', 'b', 'c', 'd', 'e'); -- Assumindo até 5 opções para múltipla escolha

-- 4. Tabela User
CREATE TABLE "User" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 5. Tabela Session (para tokens de autenticação)
CREATE TABLE "Session" (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "User"(id) ON DELETE CASCADE,
    token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 6. Tabela Challenge
CREATE TABLE "Challenge" (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "User"(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    subject VARCHAR(100) NOT NULL,
    description TEXT,
    daily_time INTEGER NOT NULL, -- Tempo diário em minutos
    duration INTEGER NOT NULL, -- Duração em dias
    photo_url VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 7. Tabela Summary (Registro Diário)
CREATE TABLE "Summary" (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "User"(id) ON DELETE CASCADE,
    challenge_id INTEGER REFERENCES "Challenge"(id) ON DELETE SET NULL, -- Opcional
    study_date DATE NOT NULL,
    study_time INTEGER NOT NULL, -- Tempo de estudo em minutos
    difficulty VARCHAR(50) NOT NULL, -- Alterado de ENUM para VARCHAR (Fácil, Médio, Difícil)
    summary_text TEXT NOT NULL,
    photo_url VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Garante que o usuário só tenha um resumo por dia
    UNIQUE (user_id, study_date)
);

-- 8. Tabela SummaryObjective (Para normalizar os objetivos alcançados)
CREATE TABLE "SummaryObjective" (
    id SERIAL PRIMARY KEY,
    summary_id INTEGER REFERENCES "Summary"(id) ON DELETE CASCADE,
    objective_text VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 9. Tabela Question (Agora linkada a Summary ao invés de Challenge)
CREATE TABLE "Question" (
    id SERIAL PRIMARY KEY,
    summary_id INTEGER REFERENCES "Summary"(id) ON DELETE CASCADE,
    text TEXT NOT NULL,
    options JSONB NOT NULL, -- Armazena as opções de múltipla escolha (ex: {"a": "Opção A", "b": "Opção B"})
    correct_answer answer_option NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 10. Tabela TestResult
CREATE TABLE "TestResult" (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "User"(id) ON DELETE CASCADE,
    summary_id INTEGER REFERENCES "Summary"(id) ON DELETE CASCADE,
    score INTEGER NOT NULL, -- Pontuação (0-100)
    correct_count INTEGER NOT NULL,
    total_count INTEGER NOT NULL,
    time_spent INTEGER, -- Tempo gasto no teste em minutos
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 11. Tabela Answer (Respostas individuais do usuário)
CREATE TABLE "Answer" (
    id SERIAL PRIMARY KEY,
    test_result_id INTEGER REFERENCES "TestResult"(id) ON DELETE CASCADE,
    question_id INTEGER REFERENCES "Question"(id) ON DELETE CASCADE,
    user_answer answer_option NOT NULL,
    is_correct BOOLEAN NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Garante que o usuário só responda a mesma pergunta uma vez por teste
    UNIQUE (test_result_id, question_id)
);

-- 12. Índice para otimizar consultas comuns
CREATE INDEX idx_summary_user_date ON "Summary" (user_id, study_date);
CREATE INDEX idx_challenge_user ON "Challenge" (user_id);
CREATE INDEX idx_question_summary ON "Question" (summary_id);
CREATE INDEX idx_testresult_user_summary ON "TestResult" (user_id, summary_id);

-- 13. Função para atualizar automaticamente o campo updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 14. Triggers para as tabelas que possuem updated_at
CREATE TRIGGER update_user_updated_at BEFORE UPDATE ON "User" FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_challenge_updated_at BEFORE UPDATE ON "Challenge" FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_summary_updated_at BEFORE UPDATE ON "Summary" FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();