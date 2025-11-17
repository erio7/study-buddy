/**
 * StudyBuddy API Client
 * Gerencia todas as requisições ao backend
 * 
 * Uso:
 * const api = new StudyBuddyAPI();
 * api.login('email@example.com', 'senha')
 */

const API_BASE_URL = 'http://localhost:8000/api';

class StudyBuddyAPI {
  constructor() {
    this.token = localStorage.getItem('authToken');
  }

  /**
   * Método auxiliar para fazer requisições HTTP
   * @param {string} endpoint - Endpoint da API (ex: '/auth/login')
   * @param {object} options - Opções do fetch (method, body, headers, etc)
   * @returns {Promise} Resposta da API em JSON
   */
  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers
    };

    // Adicionar token JWT se existir
    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers
      });

      // Se não autenticado (401), limpar token e redirecionar
      if (response.status === 401) {
        localStorage.removeItem('authToken');
        this.token = null;
        window.location.href = '/login.html';
        return null;
      }

      const data = await response.json();

      // Se resposta não foi OK, lançar erro
      if (!response.ok) {
        throw new Error(data.detail || 'Erro na requisição');
      }

      return data;
    } catch (error) {
      console.error('Erro na API:', error);
      throw error;
    }
  }

  // ==========================================
  // AUTENTICAÇÃO
  // ==========================================

  /**
   * Registrar novo usuário
   * @param {string} username - Nome de usuário
   * @param {string} email - Email do usuário
   * @param {string} password - Senha do usuário
   * @returns {Promise} Dados do usuário e token
   */
  async register(username, email, password) {
    const data = await this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ username, email, password })
    });

    if (data && data.access_token) {
      this.token = data.access_token;
      localStorage.setItem('authToken', this.token);
    }

    return data;
  }

  /**
   * Fazer login
   * @param {string} email - Email do usuário
   * @param {string} password - Senha do usuário
   * @returns {Promise} Dados do usuário e token
   */
  async login(email, password) {
    const data = await this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password })
    });

    if (data && data.access_token) {
      this.token = data.access_token;
      localStorage.setItem('authToken', this.token);
    }

    return data;
  }

  /**
   * Fazer logout
   */
  logout() {
    this.token = null;
    localStorage.removeItem('authToken');
    window.location.href = '/login.html';
  }

  /**
   * Verificar se está autenticado
   * @returns {boolean} True se tem token, false caso contrário
   */
  isAuthenticated() {
    return !!this.token;
  }

  // ==========================================
  // DESAFIOS (Challenges)
  // ==========================================

  /**
   * Criar novo desafio
   * @param {string} name - Nome do desafio
   * @param {string} subject - Disciplina/Assunto
   * @param {string} description - Descrição do desafio
   * @param {number} dailyTime - Tempo diário em minutos
   * @param {number} duration - Duração em dias
   * @param {string} photoUrl - URL da foto (opcional)
   * @returns {Promise} Dados do desafio criado
   */
  async createChallenge(name, subject, description, dailyTime, duration, photoUrl = null) {
    return this.request('/challenges', {
      method: 'POST',
      body: JSON.stringify({
        name,
        subject,
        description,
        daily_time: dailyTime,
        duration,
        photo_url: photoUrl
      })
    });
  }

  /**
   * Listar todos os desafios do usuário
   * @returns {Promise} Array de desafios
   */
  async getChallenges() {
    return this.request('/challenges', {
      method: 'GET'
    });
  }

  /**
   * Obter um desafio específico
   * @param {number} id - ID do desafio
   * @returns {Promise} Dados do desafio
   */
  async getChallenge(id) {
    return this.request(`/challenges/${id}`, {
      method: 'GET'
    });
  }

  /**
   * Atualizar um desafio
   * @param {number} id - ID do desafio
   * @param {object} data - Dados a atualizar
   * @returns {Promise} Dados do desafio atualizado
   */
  async updateChallenge(id, data) {
    return this.request(`/challenges/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data)
    });
  }

  /**
   * Deletar um desafio
   * @param {number} id - ID do desafio
   * @returns {Promise} Confirmação de deleção
   */
  async deleteChallenge(id) {
    return this.request(`/challenges/${id}`, {
      method: 'DELETE'
    });
  }

  // ==========================================
  // RESUMOS (Registros Diários)
  // ==========================================

  /**
   * Criar novo resumo/registro diário
   * @param {number} challengeId - ID do desafio (opcional)
   * @param {string} date - Data (YYYY-MM-DD)
   * @param {number} studyHours - Horas de estudo
   * @param {string} difficulty - Dificuldade (Fácil, Médio, Difícil)
   * @param {string} summaryText - Texto do resumo
   * @param {string} photoUrl - URL da foto (opcional)
   * @param {array} objectives - Array de objetivos (opcional)
   * @returns {Promise} Dados do resumo criado
   */
  async createSummary(challengeId, date, studyHours, difficulty, summaryText, photoUrl = null, objectives = []) {
    return this.request('/summaries', {
      method: 'POST',
      body: JSON.stringify({
        challenge_id: challengeId,
        date,
        study_hours: studyHours,
        difficulty,
        summary_text: summaryText,
        photo_url: photoUrl,
        objectives
      })
    });
  }

  /**
   * Listar todos os resumos do usuário
   * @returns {Promise} Array de resumos
   */
  async getSummaries() {
    return this.request('/summaries', {
      method: 'GET'
    });
  }

  /**
   * Obter um resumo específico
   * @param {number} id - ID do resumo
   * @returns {Promise} Dados do resumo
   */
  async getSummary(id) {
    return this.request(`/summaries/${id}`, {
      method: 'GET'
    });
  }

  /**
   * Obter resumos de uma data específica
   * @param {string} date - Data (YYYY-MM-DD)
   * @returns {Promise} Array de resumos da data
   */
  async getSummariesByDate(date) {
    return this.request(`/summaries?date=${date}`, {
      method: 'GET'
    });
  }

  /**
   * Atualizar um resumo
   * @param {number} id - ID do resumo
   * @param {object} data - Dados a atualizar
   * @returns {Promise} Dados do resumo atualizado
   */
  async updateSummary(id, data) {
    return this.request(`/summaries/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data)
    });
  }

  /**
   * Deletar um resumo
   * @param {number} id - ID do resumo
   * @returns {Promise} Confirmação de deleção
   */
  async deleteSummary(id) {
    return this.request(`/summaries/${id}`, {
      method: 'DELETE'
    });
  }

  // ==========================================
  // PERGUNTAS (Questions)
  // ==========================================

  /**
   * Criar nova pergunta
   * @param {number} challengeId - ID do desafio
   * @param {string} text - Texto da pergunta
   * @param {array} options - Array com as opções de resposta
   * @param {string} correctAnswer - Resposta correta
   * @returns {Promise} Dados da pergunta criada
   */
  async createQuestion(challengeId, text, options, correctAnswer) {
    return this.request('/questions', {
      method: 'POST',
      body: JSON.stringify({
        challenge_id: challengeId,
        text,
        options,
        correct_answer: correctAnswer
      })
    });
  }

  /**
   * Listar perguntas de um desafio
   * @param {number} challengeId - ID do desafio
   * @returns {Promise} Array de perguntas
   */
  async getQuestions(challengeId) {
    return this.request(`/questions?challenge_id=${challengeId}`, {
      method: 'GET'
    });
  }

  /**
   * Obter uma pergunta específica
   * @param {number} id - ID da pergunta
   * @returns {Promise} Dados da pergunta
   */
  async getQuestion(id) {
    return this.request(`/questions/${id}`, {
      method: 'GET'
    });
  }

  /**
   * Atualizar uma pergunta
   * @param {number} id - ID da pergunta
   * @param {object} data - Dados a atualizar
   * @returns {Promise} Dados da pergunta atualizada
   */
  async updateQuestion(id, data) {
    return this.request(`/questions/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data)
    });
  }

  /**
   * Deletar uma pergunta
   * @param {number} id - ID da pergunta
   * @returns {Promise} Confirmação de deleção
   */
  async deleteQuestion(id) {
    return this.request(`/questions/${id}`, {
      method: 'DELETE'
    });
  }

  // ==========================================
  // RESULTADOS (Test Results)
  // ==========================================

  /**
   * Submeter respostas e obter resultado
   * @param {number} challengeId - ID do desafio
   * @param {array} answers - Array com as respostas do usuário
   * @returns {Promise} Resultado do teste (score, acertos, etc)
   */
  async submitAnswers(challengeId, answers) {
    return this.request('/results/submit', {
      method: 'POST',
      body: JSON.stringify({
        challenge_id: challengeId,
        answers
      })
    });
  }

  /**
   * Listar todos os resultados do usuário
   * @returns {Promise} Array de resultados
   */
  async getResults() {
    return this.request('/results', {
      method: 'GET'
    });
  }

  /**
   * Obter um resultado específico
   * @param {number} id - ID do resultado
   * @returns {Promise} Dados do resultado
   */
  async getResult(id) {
    return this.request(`/results/${id}`, {
      method: 'GET'
    });
  }

  /**
   * Obter resultados de um desafio específico
   * @param {number} challengeId - ID do desafio
   * @returns {Promise} Array de resultados do desafio
   */
  async getResultsByChallenge(challengeId) {
    return this.request(`/results?challenge_id=${challengeId}`, {
      method: 'GET'
    });
  }

  // ==========================================
  // DASHBOARD
  // ==========================================

  /**
   * Obter dias com estudo (para o calendário)
   * @returns {Promise} Array de datas com estudo
   */
  async getStreakDays() {
    return this.request('/streak-days', {
      method: 'GET'
    });
  }

  /**
   * Obter dados de um dia específico
   * @param {string} date - Data (YYYY-MM-DD)
   * @returns {Promise} Dados do dia (resumos, desafios, etc)
   */
  async getDayData(date) {
    return this.request(`/day/${date}`, {
      method: 'GET'
    });
  }

  /**
   * Obter visão geral do dashboard
   * @returns {Promise} Dados do dashboard (total de desafios, horas estudadas, etc)
   */
  async getDashboardOverview() {
    return this.request('/dashboard/overview', {
      method: 'GET'
    });
  }

  // ==========================================
  // UTILITÁRIOS
  // ==========================================

  /**
   * Verificar saúde da API
   * @returns {Promise} Status da API
   */
  async healthCheck() {
    return this.request('/health', {
      method: 'GET'
    });
  }

  /**
   * Obter dados do usuário atual
   * @returns {Promise} Dados do usuário autenticado
   */
  async getCurrentUser() {
    return this.request('/users/me', {
      method: 'GET'
    });
  }

  /**
   * Atualizar perfil do usuário
   * @param {object} data - Dados a atualizar (username, email, etc)
   * @returns {Promise} Dados do usuário atualizado
   */
  async updateProfile(data) {
    return this.request('/users/me', {
      method: 'PUT',
      body: JSON.stringify(data)
    });
  }
}

// Criar instância global da API
const api = new StudyBuddyAPI();

// Exportar para uso em outros scripts
if (typeof module !== 'undefined' && module.exports) {
  module.exports = StudyBuddyAPI;
}