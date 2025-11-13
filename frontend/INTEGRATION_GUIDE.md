# 🔗 Guia de Integração com Backend

Este documento descreve como integrar o StudyBuddy com seu backend, permitindo persistência de dados e funcionalidades dinâmicas.

---

## 📋 Pontos de Integração

### 1. **Calendário com Dados Dinâmicos**

**Arquivo:** `js/calendar.js`

**Localização atual:** Linhas 24-31 (dados hardcoded)

```javascript
// ANTES (dados estáticos)
const streakDays = new Set([
  '2025-11-01', '2025-11-02', '2025-11-03', // ...
]);
```

**Como integrar:**

```javascript
// DEPOIS (dados do backend)
async function loadStreakDays() {
  try {
    const response = await fetch('/api/streak-days');
    const data = await response.json();
    return new Set(data.dates);
  } catch (error) {
    console.error('Erro ao carregar streak days:', error);
    return new Set();
  }
}

// Chamar antes de renderizar o calendário
const streakDays = await loadStreakDays();
```

**Endpoint esperado:**
```
GET /api/streak-days
Response: { "dates": ["2025-11-01", "2025-11-02", ...] }
```

---

### 2. **Navegação para Dia do Calendário**

**Arquivo:** `js/calendar.js`

**Função:** `handleDayClick(dateStr)` (linhas 151-167)

**Comportamento atual:** Abre `day-view.html?date=2025-11-13`

**Dados esperados em `day-view.html`:**

```javascript
// Adicionar no day-view.html para carregar dados do backend
async function loadDayData(dateStr) {
  try {
    const response = await fetch(`/api/day/${dateStr}`);
    const data = await response.json();
    
    // Atualizar página com dados
    document.getElementById('day-title').textContent = data.formattedDate;
    document.querySelector('[data-study-time]').textContent = data.studyTime;
    document.querySelector('[data-subject]').textContent = data.subject;
    // ... etc
    
    return data;
  } catch (error) {
    console.error('Erro ao carregar dia:', error);
  }
}

// Chamar ao carregar a página
const urlParams = new URLSearchParams(window.location.search);
const dateParam = urlParams.get('date');
if (dateParam) {
  loadDayData(dateParam);
}
```

**Endpoint esperado:**
```
GET /api/day/2025-11-13
Response: {
  "date": "2025-11-13",
  "formattedDate": "13 de Novembro, 2025",
  "studyTime": "2h 30m",
  "subject": "Química Orgânica",
  "difficulty": "Médio",
  "summary": "Estudei grupos funcionais...",
  "photo": "https://...",
  "objectives": ["Entendi os conceitos", "Resolvi exercícios", ...],
  "completed": true
}
```

---

### 3. **Criar Desafio**

**Arquivo:** `create-challenge.html`

**Formulário ID:** `challenge-form`

**Como integrar:**

```javascript
// Adicionar em app.js ou em um script específico
document.getElementById('challenge-form')?.addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const formData = new FormData(e.target);
  
  try {
    const response = await fetch('/api/challenges', {
      method: 'POST',
      body: formData // Inclui arquivo de foto
    });
    
    if (response.ok) {
      const data = await response.json();
      window.StudyBuddy.showNotification('Desafio criado com sucesso!', 'success');
      setTimeout(() => {
        window.location.href = 'challenge-detail.html?id=' + data.id;
      }, 1500);
    } else {
      window.StudyBuddy.showNotification('Erro ao criar desafio', 'error');
    }
  } catch (error) {
    console.error('Erro:', error);
    window.StudyBuddy.showNotification('Erro na requisição', 'error');
  }
});
```

**Endpoint esperado:**
```
POST /api/challenges
Content-Type: multipart/form-data

Body:
- challenge-name: string
- subject: string
- description: string (opcional)
- daily-time: number
- duration: number
- challenge-photo: file (opcional)

Response: {
  "id": "uuid",
  "name": "Desafio de Química Orgânica",
  "createdAt": "2025-11-12T20:00:00Z"
}
```

---

### 4. **Registrar Resumo Diário**

**Arquivo:** `resumo.html`

**Formulário ID:** `resumo-form`

**Como integrar:**

```javascript
document.getElementById('resumo-form')?.addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const formData = new FormData(e.target);
  
  try {
    const response = await fetch('/api/summaries', {
      method: 'POST',
      body: formData
    });
    
    if (response.ok) {
      window.StudyBuddy.showNotification('Resumo salvo com sucesso!', 'success');
      e.target.reset();
      // Recarregar lista de resumos
      loadRecentSummaries();
    }
  } catch (error) {
    window.StudyBuddy.showNotification('Erro ao salvar resumo', 'error');
  }
});
```

**Endpoint esperado:**
```
POST /api/summaries
Content-Type: multipart/form-data

Body:
- study-date: date
- subject: string
- study-hours: number
- difficulty: enum (facil, medio, dificil)
- summary-text: string
- study-photo: file (opcional)
- objectives: string[] (checkboxes selecionadas)

Response: {
  "id": "uuid",
  "date": "2025-11-13",
  "createdAt": "2025-11-12T20:00:00Z"
}
```

---

### 5. **Enviar Respostas de Perguntas**

**Arquivo:** `questions.html`

**Formulário ID:** `questions-form`

**Como integrar:**

```javascript
document.getElementById('questions-form')?.addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const answers = {
    q1: document.querySelector('input[name="q1"]:checked')?.value,
    q2: document.querySelector('input[name="q2"]:checked')?.value,
    q3: document.querySelector('input[name="q3"]:checked')?.value,
    q4: document.querySelector('input[name="q4"]:checked')?.value,
    q5: document.querySelector('input[name="q5"]:checked')?.value,
  };
  
  try {
    const response = await fetch('/api/challenges/1/answers', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(answers)
    });
    
    if (response.ok) {
      const results = await response.json();
      window.location.href = 'results.html?id=' + results.id;
    }
  } catch (error) {
    window.StudyBuddy.showNotification('Erro ao enviar respostas', 'error');
  }
});
```

**Endpoint esperado:**
```
POST /api/challenges/{challengeId}/answers
Content-Type: application/json

Body: {
  "q1": "a",
  "q2": "a",
  "q3": "a",
  "q4": "a",
  "q5": "a"
}

Response: {
  "id": "uuid",
  "score": 90,
  "correct": 18,
  "total": 20,
  "answers": [
    {
      "question": 1,
      "userAnswer": "a",
      "correctAnswer": "a",
      "isCorrect": true
    },
    // ...
  ]
}
```

---

### 6. **Carregar Resultados**

**Arquivo:** `results.html`

**Como integrar:**

```javascript
// Adicionar ao início da página
async function loadResults() {
  const urlParams = new URLSearchParams(window.location.search);
  const resultId = urlParams.get('id');
  
  if (!resultId) return;
  
  try {
    const response = await fetch(`/api/results/${resultId}`);
    const data = await response.json();
    
    // Atualizar score
    document.querySelector('.score-value').textContent = data.score + '%';
    
    // Atualizar estatísticas
    document.querySelectorAll('.stat-card')[0].querySelector('h3').textContent = data.correct;
    document.querySelectorAll('.stat-card')[1].querySelector('h3').textContent = data.total - data.correct;
    
    // Renderizar resultados por questão
    const resultsContainer = document.querySelector('[data-results-container]');
    data.answers.forEach(answer => {
      // Criar elemento para cada resposta
    });
  } catch (error) {
    console.error('Erro ao carregar resultados:', error);
  }
}

loadResults();
```

**Endpoint esperado:**
```
GET /api/results/{resultId}

Response: {
  "id": "uuid",
  "score": 90,
  "correct": 18,
  "total": 20,
  "timeSpent": "12m 45s",
  "answers": [
    {
      "questionId": 1,
      "question": "Qual é o grupo funcional...",
      "userAnswer": "a",
      "correctAnswer": "a",
      "isCorrect": true,
      "userAnswerText": "Hidroxila (-OH)",
      "correctAnswerText": "Hidroxila (-OH)"
    },
    // ...
  ]
}
```

---

## 🔐 Autenticação

Adicione headers de autenticação em todas as requisições:

```javascript
const headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer ' + localStorage.getItem('authToken')
};

fetch('/api/endpoint', {
  method: 'POST',
  headers: headers,
  body: JSON.stringify(data)
});
```

---

## 💾 Armazenamento Local (Fallback)

Para testes sem backend, use localStorage:

```javascript
// Salvar dados localmente
function saveToLocalStorage(key, data) {
  localStorage.setItem(key, JSON.stringify(data));
}

// Recuperar dados localmente
function getFromLocalStorage(key) {
  const data = localStorage.getItem(key);
  return data ? JSON.parse(data) : null;
}

// Usar como fallback
async function loadStreakDays() {
  try {
    // Tentar API
    const response = await fetch('/api/streak-days');
    return new Set((await response.json()).dates);
  } catch {
    // Fallback para localStorage
    return new Set(getFromLocalStorage('streakDays') || []);
  }
}
```

---

## 🧪 Testando Localmente

1. **Sem Backend:** Abra os arquivos HTML diretamente no navegador
2. **Com Backend Local:** Use um servidor local (Python, Node.js, etc.)
3. **Mock API:** Use bibliotecas como `msw` ou `json-server`

```bash
# Exemplo com json-server
npm install -g json-server
echo '{"streakDays": {"dates": ["2025-11-01", "2025-11-02"]}}' > db.json
json-server --watch db.json --port 3001
```

---

## 📱 Checklist de Integração

- [ ] Calendário carrega dados de streak do backend
- [ ] Clique em dia abre page com dados dinâmicos
- [ ] Criar desafio envia dados para API
- [ ] Registrar resumo persiste no backend
- [ ] Perguntas carregam do backend
- [ ] Respostas são enviadas e processadas
- [ ] Resultados mostram análise do backend
- [ ] Autenticação funciona em todas as páginas
- [ ] Tratamento de erros implementado
- [ ] Feedback visual (loading, sucesso, erro)

---

## 🚀 Próximos Passos

1. Implementar autenticação (login/registro)
2. Adicionar persistência de dados no banco
3. Implementar cronômetro funcional
4. Adicionar gráficos de progresso
5. Implementar notificações push
6. Adicionar modo offline com Service Worker

---

**Desenvolvido para facilitar a integração com seu backend!** 🎉
