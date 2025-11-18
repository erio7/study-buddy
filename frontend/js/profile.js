/**
 * StudyBuddy - Profile Page
 * Carrega e exibe os dados do perfil do usuário
 */

(function() {
  'use strict';

  const api = new StudyBuddyAPI();

  // ==========================================
  // CARREGAR DADOS DO PERFIL
  // ==========================================
  async function loadProfileData() {
    try {
      // Buscar dados do usuário (você pode precisar criar esse endpoint)
      // Por enquanto, vamos buscar dados do localStorage
      const token = localStorage.getItem('authToken');
      if (!token) {
        window.location.href = '/login.html';
        return;
      }

      // Buscar desafios e resumos
      const challenges = await api.getChallenges();
      const summaries = await api.getSummaries();
      const results = await api.getResults();

      displayProfileData(challenges, summaries, results);
    } catch (error) {
      showError('Erro ao carregar dados do perfil: ' + error.message);
      console.error(error);
    }
  }

  // ==========================================
  // EXIBIR DADOS DO PERFIL
  // ==========================================
  function displayProfileData(challenges, summaries, results) {
    // Calcular estatísticas
    const stats = calculateStats(challenges, summaries, results);

    // Atualizar cards de estatísticas
    const statCards = document.querySelectorAll('.challenge-stats .stat-card');
    if (statCards.length >= 4) {
      // Streak Atual
      statCards[0].querySelector('h3').textContent = stats.streakDays;
      statCards[0].querySelector('p').textContent = 'Streak Atual';

      // Desafios Completos
      statCards[1].querySelector('h3').textContent = stats.completedChallenges;
      statCards[1].querySelector('p').textContent = 'Desafios Completos';

      // Total de Estudo
      statCards[2].querySelector('h3').textContent = formatTime(stats.totalStudyTime);
      statCards[2].querySelector('p').textContent = 'Total de Estudo';

      // Taxa de Acerto
      statCards[3].querySelector('h3').textContent = stats.successRate + '%';
      statCards[3].querySelector('p').textContent = 'Taxa de Acerto';
    }

    // Atualizar desafios arquivados
    updateArchivedChallenges(challenges);
  }

  // ==========================================
  // CALCULAR ESTATÍSTICAS
  // ==========================================
  function calculateStats(challenges, summaries, results) {
    // Streak Atual (número de dias consecutivos com estudo)
    const streakDays = calculateStreak(summaries);

    // Desafios Completos
    const completedChallenges = challenges.filter(c => {
      const challengeSummaries = summaries.filter(s => s.challenge_id === c.id);
      return challengeSummaries.length >= c.duration;
    }).length;

    // Total de Estudo (em minutos)
    const totalStudyTime = summaries.reduce((sum, s) => sum + s.study_time, 0);

    // Taxa de Acerto
    const totalCorrect = results.reduce((sum, r) => sum + r.correct_count, 0);
    const totalQuestions = results.reduce((sum, r) => sum + r.total_count, 0);
    const successRate = totalQuestions > 0 ? Math.round((totalCorrect / totalQuestions) * 100) : 0;

    return {
      streakDays,
      completedChallenges,
      totalStudyTime,
      successRate
    };
  }

  // ==========================================
  // CALCULAR STREAK
  // ==========================================
  function calculateStreak(summaries) {
    if (summaries.length === 0) return 0;

    // Ordenar por data decrescente
    const sorted = [...summaries].sort((a, b) => {
      return new Date(b.study_date) - new Date(a.study_date);
    });

    let streak = 0;
    let currentDate = new Date();
    currentDate.setHours(0, 0, 0, 0);

    for (const summary of sorted) {
      const summaryDate = new Date(summary.study_date);
      summaryDate.setHours(0, 0, 0, 0);

      const diffTime = currentDate - summaryDate;
      const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

      if (diffDays === streak) {
        streak++;
        currentDate = new Date(summaryDate);
      } else {
        break;
      }
    }

    return streak;
  }

  // ==========================================
  // FORMATAR TEMPO
  // ==========================================
  function formatTime(minutes) {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    if (hours === 0) return `${mins}m`;
    if (mins === 0) return `${hours}h`;
    return `${hours}h ${mins}m`;
  }

  // ==========================================
  // ATUALIZAR DESAFIOS ARQUIVADOS
  // ==========================================
  function updateArchivedChallenges(challenges) {
    const progressList = document.querySelector('.progress-list');
    if (!progressList) return;

    // Limpar itens existentes
    progressList.innerHTML = '';

    // Exibir todos os desafios
    challenges.forEach(challenge => {
      const date = new Date(challenge.created_at);
      const formattedDate = date.toLocaleDateString('pt-BR', { 
        day: 'numeric', 
        month: 'long',
        year: 'numeric'
      });

      const item = document.createElement('div');
      item.className = 'progress-item';
      item.innerHTML = `
        <div class="progress-item-header">
          <span class="progress-date">${challenge.name}</span>
          <span class="progress-status">✅ Ativo</span>
        </div>
        <p class="progress-time" style="margin: 6px 0 0; color: var(--color-text-secondary);">
          Criado em ${formattedDate} • Duração: ${challenge.duration} dias
        </p>
      `;
      progressList.appendChild(item);
    });
  }

  // ==========================================
  // EVENT LISTENERS
  // ==========================================
  function initEventListeners() {
    // Botão Editar Perfil
    const editProfileBtn = document.querySelector('button:has-text("Editar Perfil")');
    if (editProfileBtn) {
      editProfileBtn.addEventListener('click', () => {
        showNotification('Funcionalidade de edição de perfil em desenvolvimento', 'info');
      });
    }

    // Botão Alterar Senha
    const changePasswordBtn = document.querySelector('button:has-text("Alterar Senha")');
    if (changePasswordBtn) {
      changePasswordBtn.addEventListener('click', () => {
        showNotification('Funcionalidade de alteração de senha em desenvolvimento', 'info');
      });
    }

    // Botão Logout (se existir)
    const logoutBtn = document.querySelector('button:has-text("Logout")');
    if (logoutBtn) {
      logoutBtn.addEventListener('click', () => {
        api.logout();
      });
    }
  }

  // ==========================================
  // MOSTRAR NOTIFICAÇÃO
  // ==========================================
  function showError(message) {
    window.StudyBuddy.showNotification(message, 'error');
  }

  function showNotification(message, type = 'info') {
    window.StudyBuddy.showNotification(message, type);
  }

  // ==========================================
  // INICIALIZAÇÃO
  // ==========================================
  async function init() {
    await loadProfileData();
    initEventListeners();
  }

  // Executar quando o DOM estiver pronto
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
