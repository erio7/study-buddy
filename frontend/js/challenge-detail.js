/**
 * StudyBuddy - Challenge Detail Page
 * Carrega e exibe os dados de um desafio específico
 */

(function() {
  'use strict';

  const api = new StudyBuddyAPI();

  // ==========================================
  // OBTER ID DA URL
  // ==========================================
  function getChallengeIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    const id = params.get('id');
    
    if (!id) {
      showError('ID do desafio não encontrado na URL');
      return null;
    }
    
    return parseInt(id);
  }

  // ==========================================
  // CARREGAR DADOS DO DESAFIO
  // ==========================================
  async function loadChallengeData(challengeId) {
    try {
      const challenge = await api.getChallenge(challengeId);
      const summaries = await api.getSummaries();
      const results = await api.getResults();
      
      // Filtrar dados do desafio específico
      const challengeSummaries = summaries.filter(s => s.challenge_id === challengeId);
      const challengeResults = results.filter(r => {
        // Encontrar o resumo correspondente
        const summary = summaries.find(s => s.id === r.summary_id);
        return summary && summary.challenge_id === challengeId;
      });
      
      displayChallengeData(challenge, challengeSummaries, challengeResults);
    } catch (error) {
      showError('Erro ao carregar dados do desafio: ' + error.message);
      console.error(error);
    }
  }

  // ==========================================
  // EXIBIR DADOS DO DESAFIO
  // ==========================================
  function displayChallengeData(challenge, summaries, results) {
    // Atualizar título e descrição
    const titleElement = document.querySelector('h1');
    if (titleElement) {
      titleElement.textContent = challenge.name;
    }

    const descElement = document.querySelector('main > div > p');
    if (descElement) {
      const createdDate = new Date(challenge.created_at).toLocaleDateString('pt-BR');
      descElement.textContent = `Iniciado em ${createdDate} • ${challenge.duration} dias de duração`;
    }

    // Calcular estatísticas
    const stats = calculateStats(challenge, summaries, results);

    // Atualizar cards de estatísticas
    const statCards = document.querySelectorAll('.stat-card');
    if (statCards.length >= 4) {
      // Progresso Geral
      statCards[0].querySelector('h3').textContent = stats.progress + '%';
      statCards[0].querySelector('p').textContent = 'Progresso Geral';

      // Dias Completados
      statCards[1].querySelector('h3').textContent = stats.daysCompleted + '/' + challenge.duration;
      statCards[1].querySelector('p').textContent = 'Dias Completados';

      // Tempo Total
      statCards[2].querySelector('h3').textContent = formatTime(stats.totalTime);
      statCards[2].querySelector('p').textContent = 'Tempo Total';

      // Questões Acertadas
      statCards[3].querySelector('h3').textContent = stats.correctAnswers + '/' + stats.totalQuestions;
      statCards[3].querySelector('p').textContent = 'Questões Acertadas';
    }

    // Atualizar barra de progresso
    updateProgressBars(stats);

    // Atualizar lista de progresso recente
    updateRecentProgress(summaries);
  }

  // ==========================================
  // CALCULAR ESTATÍSTICAS
  // ==========================================
  function calculateStats(challenge, summaries, results) {
    // Progresso Geral (dias completados / dias totais * 100)
    const daysCompleted = summaries.length;
    const progress = Math.round((daysCompleted / challenge.duration) * 100);

    // Tempo Total (soma de todos os study_time)
    const totalTime = summaries.reduce((sum, s) => sum + s.study_time, 0);

    // Questões Acertadas (soma de correct_count)
    const correctAnswers = results.reduce((sum, r) => sum + r.correct_count, 0);
    const totalQuestions = results.reduce((sum, r) => sum + r.total_count, 0);

    return {
      progress: Math.min(progress, 100), // Máximo 100%
      daysCompleted,
      totalTime,
      correctAnswers,
      totalQuestions: totalQuestions || 0
    };
  }

  // ==========================================
  // FORMATAR TEMPO
  // ==========================================
  function formatTime(minutes) {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return `${hours}h ${mins}m`;
  }

  // ==========================================
  // ATUALIZAR BARRAS DE PROGRESSO
  // ==========================================
  function updateProgressBars(stats) {
    const progressBars = document.querySelectorAll('.card div[style*="linear-gradient"]');
    
    if (progressBars.length >= 2) {
      // Primeira barra (Conclusão Geral)
      progressBars[0].style.width = stats.progress + '%';

      // Segunda barra (Questões Respondidas)
      const questionsPercentage = stats.totalQuestions > 0 
        ? Math.round((stats.correctAnswers / stats.totalQuestions) * 100)
        : 0;
      progressBars[1].style.width = questionsPercentage + '%';

      // Atualizar textos das porcentagens
      const percentageTexts = document.querySelectorAll('.card span[style*="font-weight: 600"]');
      if (percentageTexts.length >= 2) {
        percentageTexts[0].textContent = stats.progress + '%';
        percentageTexts[1].textContent = questionsPercentage + '%';
      }
    }
  }

  // ==========================================
  // ATUALIZAR PROGRESSO RECENTE
  // ==========================================
  function updateRecentProgress(summaries) {
    const progressList = document.querySelector('.progress-list');
    if (!progressList) return;

    // Limpar itens existentes
    progressList.innerHTML = '';

    // Ordenar por data decrescente (mais recente primeiro)
    const sortedSummaries = [...summaries].sort((a, b) => {
      return new Date(b.study_date) - new Date(a.study_date);
    });

    // Exibir últimos 5 resumos
    sortedSummaries.slice(0, 5).forEach(summary => {
      const date = new Date(summary.study_date);
      const formattedDate = date.toLocaleDateString('pt-BR', { 
        day: 'numeric', 
        month: 'long' 
      });

      const item = document.createElement('div');
      item.className = 'progress-item';
      item.innerHTML = `
        <div class="progress-item-header">
          <span class="progress-date">${formattedDate}</span>
          <span class="progress-status">✅ Concluído</span>
        </div>
        <p class="progress-time" style="margin: 6px 0 0; color: var(--color-text-secondary);">
          ${formatTime(summary.study_time)} de estudo • Dificuldade: ${summary.difficulty}
        </p>
      `;
      progressList.appendChild(item);
    });
  }

  // ==========================================
  // MOSTRAR ERRO
  // ==========================================
  function showError(message) {
    window.StudyBuddy.showNotification(message, 'error');
  }

  // ==========================================
  // INICIALIZAÇÃO
  // ==========================================
  async function init() {
    const challengeId = getChallengeIdFromURL();
    
    if (challengeId) {
      await loadChallengeData(challengeId);
    }
  }

  // Executar quando o DOM estiver pronto
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
