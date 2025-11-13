/**
 * StudyBuddy - Funcionalidades Gerais
 * Melhorias de UX e interatividade
 */

(function() {
  'use strict';

  // ==========================================
  // NAVEGAÇÃO ATIVA
  // ==========================================
  function setActiveNavLink() {
    const currentPage = window.location.pathname.split('/').pop() || 'home.html';
    const navLinks = document.querySelectorAll('.hotbar-link');
    
    navLinks.forEach(link => {
      const href = link.getAttribute('href');
      if (href === currentPage) {
        link.classList.add('active');
        link.setAttribute('aria-current', 'page');
      } else {
        link.classList.remove('active');
        link.removeAttribute('aria-current');
      }
    });
  }

  // ==========================================
  // ANIMAÇÕES DE CARDS
  // ==========================================
  function initCardAnimations() {
    const cards = document.querySelectorAll('.card');
    
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry, index) => {
        if (entry.isIntersecting) {
          setTimeout(() => {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
          }, index * 100);
          observer.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.1
    });

    cards.forEach(card => {
      card.style.opacity = '0';
      card.style.transform = 'translateY(20px)';
      card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
      observer.observe(card);
    });
  }

  // ==========================================
  // VALIDAÇÃO DE FORMULÁRIOS
  // ==========================================
  function initFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
      form.addEventListener('submit', function(e) {
        const requiredFields = form.querySelectorAll('[required]');
        let isValid = true;

        requiredFields.forEach(field => {
          if (!field.value.trim()) {
            isValid = false;
            field.style.borderColor = '#ef4444';
            
            // Remover erro ao digitar
            field.addEventListener('input', function() {
              this.style.borderColor = '';
            }, { once: true });
          }
        });

        if (!isValid) {
          e.preventDefault();
          showNotification('Por favor, preencha todos os campos obrigatórios', 'error');
        }
      });
    });
  }

  // ==========================================
  // SISTEMA DE NOTIFICAÇÕES
  // ==========================================
  function showNotification(message, type = 'info') {
    // Remover notificação anterior se existir
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
      existingNotification.remove();
    }

    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Estilos inline para garantir funcionamento
    Object.assign(notification.style, {
      position: 'fixed',
      top: '24px',
      right: '24px',
      padding: '16px 24px',
      borderRadius: '12px',
      backgroundColor: type === 'error' ? '#ef4444' : type === 'success' ? '#22c55e' : '#8b5cf6',
      color: 'white',
      fontWeight: '600',
      fontSize: '15px',
      boxShadow: '0 10px 30px rgba(0,0,0,.3)',
      zIndex: '9999',
      animation: 'slideIn 0.3s ease',
      maxWidth: '400px'
    });

    document.body.appendChild(notification);

    // Remover após 3 segundos
    setTimeout(() => {
      notification.style.animation = 'slideOut 0.3s ease';
      setTimeout(() => notification.remove(), 300);
    }, 3000);
  }

  // Adicionar animações CSS
  const style = document.createElement('style');
  style.textContent = `
    @keyframes slideIn {
      from {
        transform: translateX(400px);
        opacity: 0;
      }
      to {
        transform: translateX(0);
        opacity: 1;
      }
    }
    @keyframes slideOut {
      from {
        transform: translateX(0);
        opacity: 1;
      }
      to {
        transform: translateX(400px);
        opacity: 0;
      }
    }
  `;
  document.head.appendChild(style);

  // ==========================================
  // UPLOAD DE ARQUIVO COM PREVIEW
  // ==========================================
  function initFileUpload() {
    const uploadAreas = document.querySelectorAll('.upload-area');
    
    uploadAreas.forEach(area => {
      const input = area.querySelector('input[type="file"]');
      if (!input) return;

      // Click na área para abrir seletor
      area.addEventListener('click', () => input.click());

      // Drag and drop
      area.addEventListener('dragover', (e) => {
        e.preventDefault();
        area.style.borderColor = 'var(--color-primary)';
        area.style.backgroundColor = 'var(--color-primary-light)';
      });

      area.addEventListener('dragleave', () => {
        area.style.borderColor = '';
        area.style.backgroundColor = '';
      });

      area.addEventListener('drop', (e) => {
        e.preventDefault();
        area.style.borderColor = '';
        area.style.backgroundColor = '';
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
          input.files = files;
          handleFileSelect(files[0], area);
        }
      });

      // Seleção de arquivo
      input.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
          handleFileSelect(e.target.files[0], area);
        }
      });
    });
  }

  function handleFileSelect(file, area) {
    if (file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = (e) => {
        // Criar preview
        const preview = document.createElement('div');
        preview.style.cssText = 'margin-top: 16px; text-align: center;';
        preview.innerHTML = `
          <img src="${e.target.result}" alt="Preview" style="max-width: 100%; max-height: 200px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,.2);">
          <p style="margin-top: 12px; font-size: 14px; color: var(--color-text-secondary);">${file.name}</p>
        `;
        
        // Remover preview anterior
        const existingPreview = area.querySelector('div[style*="margin-top"]');
        if (existingPreview) existingPreview.remove();
        
        area.appendChild(preview);
      };
      reader.readAsDataURL(file);
    } else {
      showNotification('Por favor, selecione uma imagem válida', 'error');
    }
  }

  // ==========================================
  // SMOOTH SCROLL
  // ==========================================
  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function(e) {
        const href = this.getAttribute('href');
        if (href === '#') return;
        
        e.preventDefault();
        const target = document.querySelector(href);
        if (target) {
          target.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
        }
      });
    });
  }

  // ==========================================
  // LOADING STATE PARA BOTÕES
  // ==========================================
  function initButtonLoading() {
    document.querySelectorAll('button[type="submit"], .btn-primary').forEach(btn => {
      btn.addEventListener('click', function() {
        if (this.classList.contains('loading')) return;
        
        const form = this.closest('form');
        if (form && !form.checkValidity()) return;
        
        this.classList.add('loading');
        this.disabled = true;
        const originalText = this.textContent;
        this.textContent = 'Carregando...';
        
        // Simular loading (remover em produção com backend real)
        setTimeout(() => {
          this.classList.remove('loading');
          this.disabled = false;
          this.textContent = originalText;
        }, 2000);
      });
    });
  }

  // ==========================================
  // TOOLTIPS
  // ==========================================
  function initTooltips() {
    document.querySelectorAll('[title]').forEach(el => {
      el.addEventListener('mouseenter', function(e) {
        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip';
        tooltip.textContent = this.getAttribute('title');
        tooltip.style.cssText = `
          position: absolute;
          background: rgba(0,0,0,.9);
          color: white;
          padding: 8px 12px;
          border-radius: 6px;
          font-size: 13px;
          pointer-events: none;
          z-index: 10000;
          white-space: nowrap;
        `;
        
        document.body.appendChild(tooltip);
        
        const rect = this.getBoundingClientRect();
        tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
        tooltip.style.top = rect.top - tooltip.offsetHeight - 8 + 'px';
        
        this.addEventListener('mouseleave', () => tooltip.remove(), { once: true });
      });
    });
  }

  // ==========================================
  // INICIALIZAÇÃO
  // ==========================================
  function init() {
    setActiveNavLink();
    initCardAnimations();
    initFormValidation();
    initFileUpload();
    initSmoothScroll();
    initButtonLoading();
    initTooltips();
    
    console.log('StudyBuddy inicializado com sucesso! 🚀');
  }

  // Executar quando o DOM estiver pronto
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Exportar funções úteis
  window.StudyBuddy = {
    showNotification: showNotification
  };

})();
