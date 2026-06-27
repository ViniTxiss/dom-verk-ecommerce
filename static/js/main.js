// DOM VERK — main.js
document.addEventListener('DOMContentLoaded', () => {

  // ─── NAVBAR SCROLL ───
  const navbar = document.getElementById('navbar');
  const announceHeight = document.querySelector('.announce-bar')?.offsetHeight || 36;

  window.addEventListener('scroll', () => {
    if (window.scrollY > announceHeight) {
      navbar?.classList.add('scrolled');
    } else {
      navbar?.classList.remove('scrolled');
    }
  }, { passive: true });

  // ─── SEARCH TOGGLE ───
  const searchToggle = document.getElementById('search-toggle');
  const searchBar = document.getElementById('search-bar');
  const searchInput = document.getElementById('search-input');

  searchToggle?.addEventListener('click', () => {
    const isOpen = searchBar.classList.toggle('open');
    if (isOpen) {
      setTimeout(() => searchInput?.focus(), 300);
    }
  });

  // Close search on Escape
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      searchBar?.classList.remove('open');
      closeMobileMenu();
      closeCartDrawer();
    }
  });

  // ─── MOBILE MENU ───
  const mobileToggle = document.getElementById('mobile-toggle');
  const mobileClose = document.getElementById('mobile-close');
  const mobileMenu = document.getElementById('mobile-menu');
  const mobileOverlay = document.getElementById('mobile-overlay');

  window.closeMobileMenu = function () {
    mobileMenu?.classList.remove('open');
    mobileOverlay?.classList.remove('open');
    document.body.style.overflow = '';
  };

  mobileToggle?.addEventListener('click', () => {
    mobileMenu?.classList.add('open');
    mobileOverlay?.classList.add('open');
    document.body.style.overflow = 'hidden';
  });

  mobileClose?.addEventListener('click', closeMobileMenu);
  mobileOverlay?.addEventListener('click', closeMobileMenu);

  // ─── AUTO DISMISS MESSAGES ───
  const messages = document.querySelectorAll('.message');
  messages.forEach((msg, i) => {
    setTimeout(() => {
      msg.style.animation = 'none';
      msg.style.opacity = '0';
      msg.style.transform = 'translateY(10px)';
      msg.style.transition = 'all 0.3s ease';
      setTimeout(() => msg.remove(), 300);
    }, 5000 + i * 500);
  });

  // ─── PRODUCT CARD QUICK ADD MODAL ───
  window.openQuickAdd = function (productId, productName, price) {
    // Cria modal dinâmico de seleção de tamanho
    const existing = document.getElementById('quick-add-modal');
    existing?.remove();

    const modal = document.createElement('div');
    modal.id = 'quick-add-modal';
    modal.style.cssText = `
      position: fixed; inset: 0; z-index: 500;
      background: rgba(0,0,0,0.7);
      display: flex; align-items: center; justify-content: center;
      padding: 1rem;
    `;

    modal.innerHTML = `
      <div style="
        background: var(--surface);
        border: 1px solid var(--border);
        padding: 2rem;
        max-width: 420px;
        width: 100%;
        animation: slideUp 0.3s ease;
      ">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.5rem;">
          <div>
            <h3 style="font-size: 1rem; font-weight: 700; margin-bottom: 0.25rem;">${productName}</h3>
            <p style="color: var(--accent); font-weight: 700; font-size: 1.1rem;">R$ ${parseFloat(price).toFixed(2).replace('.', ',')}</p>
          </div>
          <button onclick="document.getElementById('quick-add-modal').remove()" style="color: var(--text-muted); font-size: 1.2rem; padding: 0.25rem;">✕</button>
        </div>
        <p style="font-size: 0.75rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--text-muted); margin-bottom: 1rem;">Tamanho</p>
        <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 1.5rem;" id="size-grid">
          ${['PP', 'P', 'M', 'G', 'GG', '2GG', '3GG', '4GG'].map(s => `
            <button
              class="size-btn"
              data-size="${s}"
              onclick="selectSize(this, '${s}')"
              style="
                border: 1px solid var(--border);
                background: transparent;
                color: var(--text);
                padding: 0.5rem 1rem;
                font-family: var(--font-head);
                font-size: 0.8rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s;
              "
            >${s}</button>
          `).join('')}
        </div>
        <button
          id="quick-add-confirm"
          onclick="quickAddToCart(${productId})"
          class="btn btn--accent btn--full"
          disabled
          style="opacity: 0.5;"
        >Selecione um tamanho</button>
      </div>
    `;

    document.body.appendChild(modal);
    modal.addEventListener('click', (e) => {
      if (e.target === modal) modal.remove();
    });
  };

  window._selectedSize = null;

  window.selectSize = function (btn, size) {
    document.querySelectorAll('.size-btn').forEach(b => {
      b.style.background = 'transparent';
      b.style.borderColor = 'var(--border)';
      b.style.color = 'var(--text)';
    });
    btn.style.background = 'var(--accent)';
    btn.style.borderColor = 'var(--accent)';
    btn.style.color = '#0C0C0C';
    window._selectedSize = size;

    const confirmBtn = document.getElementById('quick-add-confirm');
    if (confirmBtn) {
      confirmBtn.textContent = 'Adicionar ao Carrinho';
      confirmBtn.disabled = false;
      confirmBtn.style.opacity = '1';
    }
  };

  window.quickAddToCart = function (productId) {
    // Adicionar ao carrinho via AJAX sem variante específica (simplified)
    fetch('/carrinho/adicionar/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrf() },
      body: JSON.stringify({ product_id: productId, variant_id: null, quantity: 1 })
    })
    .then(r => r.json())
    .then(data => {
      if (data.success) {
        document.getElementById('quick-add-modal')?.remove();
        updateCartBadge(data.cart_count);
        showNotification(data.message || 'Produto adicionado!');
        openCartDrawer();
      }
    })
    .catch(() => {
      // Fallback: redirect to product page
      window.location.href = `/produto/${productId}/`;
    });
  };

  // ─── CSRF ───
  window.getCsrf = function () {
    return document.cookie.split('; ')
      .find(r => r.startsWith('csrftoken='))
      ?.split('=')[1] || '';
  };

  // ─── NOTIFICATIONS ───
  window.showNotification = function (msg, type = 'success') {
    const container = document.getElementById('messages-container') || (() => {
      const el = document.createElement('div');
      el.id = 'messages-container';
      el.className = 'messages-container';
      document.body.appendChild(el);
      return el;
    })();

    const el = document.createElement('div');
    el.className = `message message--${type}`;
    el.innerHTML = `<span>${msg}</span><button class="message__close" onclick="this.parentElement.remove()">✕</button>`;
    container.appendChild(el);

    setTimeout(() => {
      el.style.transition = 'all 0.3s ease';
      el.style.opacity = '0';
      el.style.transform = 'translateY(10px)';
      setTimeout(() => el.remove(), 300);
    }, 4000);
  };

  // ─── CART BADGE UPDATE ───
  window.updateCartBadge = function (count) {
    const badge = document.getElementById('cart-badge');
    if (!badge) return;
    badge.textContent = count;
    if (count > 0) {
      badge.classList.remove('cart-badge--hidden');
      badge.style.animation = 'none';
      badge.offsetHeight; // reflow
      badge.style.animation = 'scalePop 0.3s ease';
    } else {
      badge.classList.add('cart-badge--hidden');
    }
  };

});
