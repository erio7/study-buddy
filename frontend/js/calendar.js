/**
 * StudyBuddy - Calendário Interativo Otimizado
 * Navegação por mês com indicadores visuais de streak
 */

(function() {
  'use strict';

  // Elementos do DOM
  const calendarEl = document.getElementById('calendar');
  const titleEl = document.getElementById('calendar-title');
  const prevBtn = document.getElementById('prev-month');
  const nextBtn = document.getElementById('next-month');

  // Verificar se os elementos existem
  if (!calendarEl || !titleEl || !prevBtn || !nextBtn) {
    console.warn('Elementos do calendário não encontrados');
    return;
  }

  // Configurações
  const monthNames = [
    'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
  ];

  const dayHeaders = ['S', 'T', 'Q', 'Q', 'S', 'S', 'D'];

  // Estado atual
  let currentDate = new Date();

  // Dias com streak (exemplo - pode ser carregado de localStorage ou API)
  const streakDays = new Set([
    '2025-11-01', '2025-11-02', '2025-11-03', '2025-11-04', '2025-11-05',
    '2025-11-06', '2025-11-07', '2025-11-08', '2025-11-09', '2025-11-10',
    '2025-11-11', '2025-11-12', '2025-11-13'
  ]);

  /**
   * Renderiza o calendário para o mês especificado
   * @param {Date} date - Data do mês a ser renderizado
   */
  function renderCalendar(date) {
    // Limpar calendário
    calendarEl.innerHTML = '';

    const year = date.getFullYear();
    const month = date.getMonth();
    const today = new Date();

    // Atualizar título
    titleEl.textContent = `${monthNames[month]} ${year}`;

    // Adicionar cabeçalhos dos dias
    dayHeaders.forEach(header => {
      const headEl = document.createElement('div');
      headEl.className = 'head';
      headEl.textContent = header;
      headEl.setAttribute('aria-label', getDayName(header));
      calendarEl.appendChild(headEl);
    });

    // Calcular dias do mês anterior
    const firstDay = new Date(year, month, 1);
    const daysInPrevMonth = new Date(year, month, 0).getDate();
    const offset = (firstDay.getDay() + 6) % 7; // Segunda = 0

    // Dias do mês anterior (faded)
    for (let i = offset; i > 0; i--) {
      const dayNum = daysInPrevMonth - i + 1;
      const dayEl = createDayElement(dayNum, true);
      calendarEl.appendChild(dayEl);
    }

    // Dias do mês atual
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    for (let day = 1; day <= daysInMonth; day++) {
      const isToday = 
        day === today.getDate() && 
        month === today.getMonth() && 
        year === today.getFullYear();
      
      const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
      const hasStreak = streakDays.has(dateStr);
      
      const dayEl = createDayElement(day, false, isToday, hasStreak, dateStr);
      calendarEl.appendChild(dayEl);
    }

    // Dias do próximo mês para completar a grade
    const totalCells = calendarEl.children.length - 7; // Subtrair headers
    const remainder = totalCells % 7;
    if (remainder !== 0) {
      const nextDays = 7 - remainder;
      for (let i = 1; i <= nextDays; i++) {
        const dayEl = createDayElement(i, true);
        calendarEl.appendChild(dayEl);
      }
    }

    // Animação de entrada
    animateCalendar();
  }

  /**
   * Cria um elemento de dia do calendário
   * @param {number} dayNum - Número do dia
   * @param {boolean} isFaded - Se o dia é de outro mês
   * @param {boolean} isToday - Se é o dia atual
   * @param {boolean} hasStreak - Se o dia tem streak
   * @param {string} dateStr - String da data (YYYY-MM-DD)
   * @returns {HTMLElement}
   */
  function createDayElement(dayNum, isFaded = false, isToday = false, hasStreak = false, dateStr = '') {
    const dayEl = document.createElement('div');
    dayEl.className = 'day';
    dayEl.textContent = dayNum;
    
    if (isFaded) {
      dayEl.classList.add('faded');
    }
    if (isToday) {
      dayEl.classList.add('current');
      dayEl.setAttribute('aria-current', 'date');
    }
    if (hasStreak) {
      dayEl.classList.add('streak');
      dayEl.setAttribute('title', 'Dia com estudo registrado');
    }
    
    if (!isFaded && dateStr) {
      dayEl.setAttribute('data-date', dateStr);
      dayEl.setAttribute('role', 'button');
      dayEl.setAttribute('tabindex', '0');
      dayEl.addEventListener('click', () => handleDayClick(dateStr));
      dayEl.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          handleDayClick(dateStr);
        }
      });
    }
    
    return dayEl;
  }

  /**
   * Handler para clique em um dia
   * @param {string} dateStr - Data clicada
   */
  function handleDayClick(dateStr) {
    console.log('Dia clicado:', dateStr);
    
    // Feedback visual com animação
    const dayEl = document.querySelector(`[data-date="${dateStr}"]`);
    if (dayEl) {
      dayEl.style.transform = 'scale(0.95)';
      setTimeout(() => {
        dayEl.style.transform = '';
      }, 150);
    }
    
    // Navegar para a página de visualização do dia com animação
    setTimeout(() => {
      window.location.href = `day-view.html?date=${dateStr}`;
    }, 150);
  }

  /**
   * Obtém o nome completo do dia da semana
   * @param {string} abbr - Abreviação do dia
   * @returns {string}
   */
  function getDayName(abbr) {
    const names = {
      'S': 'Domingo',
      'T': 'Terça-feira',
      'Q': 'Quarta-feira',
      'S': 'Sábado'
    };
    return names[abbr] || abbr;
  }

  /**
   * Anima a entrada do calendário
   */
  function animateCalendar() {
    const days = calendarEl.querySelectorAll('.day');
    days.forEach((day, index) => {
      day.style.opacity = '0';
      day.style.transform = 'scale(0.8)';
      setTimeout(() => {
        day.style.transition = 'opacity 0.2s ease, transform 0.2s ease';
        day.style.opacity = '1';
        day.style.transform = 'scale(1)';
      }, index * 10);
    });
  }

  /**
   * Navega para o mês anterior
   */
  function prevMonth() {
    currentDate.setMonth(currentDate.getMonth() - 1);
    renderCalendar(currentDate);
  }

  /**
   * Navega para o próximo mês
   */
  function nextMonth() {
    currentDate.setMonth(currentDate.getMonth() + 1);
    renderCalendar(currentDate);
  }

  // Event listeners
  prevBtn.addEventListener('click', prevMonth);
  nextBtn.addEventListener('click', nextMonth);

  // Navegação por teclado
  document.addEventListener('keydown', (e) => {
    if (e.target.closest('.calendar-header')) {
      if (e.key === 'ArrowLeft') {
        prevMonth();
      } else if (e.key === 'ArrowRight') {
        nextMonth();
      }
    }
  });

  // Renderização inicial
  renderCalendar(currentDate);

  // Atualizar streak count (exemplo)
  const streakCountEl = document.getElementById('streak-count');
  if (streakCountEl) {
    streakCountEl.textContent = streakDays.size;
  }

  // Exportar funções para uso externo (opcional)
  window.StudyBuddyCalendar = {
    addStreakDay: function(dateStr) {
      streakDays.add(dateStr);
      renderCalendar(currentDate);
    },
    removeStreakDay: function(dateStr) {
      streakDays.delete(dateStr);
      renderCalendar(currentDate);
    },
    getStreakDays: function() {
      return Array.from(streakDays);
    },
    refresh: function() {
      renderCalendar(currentDate);
    }
  };

})();
