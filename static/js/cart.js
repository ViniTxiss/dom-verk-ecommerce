// DOM VERK — cart.js
document.addEventListener('DOMContentLoaded', () => {

  // ─── CART DRAWER TOGGLE ───
  const cartToggle = document.getElementById('cart-toggle');
  const cartDrawer = document.getElementById('cart-drawer');
  const cartDrawerOverlay = document.getElementById('cart-drawer-overlay');
  const cartDrawerClose = document.getElementById('cart-drawer-close');

  window.openCartDrawer = function () {
    cartDrawer?.classList.add('open');
    cartDrawerOverlay?.classList.add('open');
    document.body.style.overflow = 'hidden';
  };

  window.closeCartDrawer = function () {
    cartDrawer?.classList.remove('open');
    cartDrawerOverlay?.classList.remove('open');
    document.body.style.overflow = '';
  };

  cartToggle?.addEventListener('click', () => {
    const isOpen = cartDrawer?.classList.contains('open');
    if (isOpen) closeCartDrawer();
    else openCartDrawer();
  });

  cartDrawerClose?.addEventListener('click', closeCartDrawer);
  cartDrawerOverlay?.addEventListener('click', closeCartDrawer);

  // ─── ADD TO CART (AJAX) ───
  window.addToCart = function (productId, variantId, quantity = 1) {
    return fetch('/carrinho/adicionar/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrf(),
      },
      body: JSON.stringify({ product_id: productId, variant_id: variantId, quantity }),
    })
    .then(r => r.json())
    .then(data => {
      if (data.success) {
        updateCartBadge(data.cart_count);
        showNotification(data.message || 'Adicionado ao carrinho!');
        // Recarrega o drawer
        reloadCartDrawer();
      } else {
        showNotification(data.error || 'Erro ao adicionar.', 'error');
      }
      return data;
    });
  };

  // ─── UPDATE CART ITEM ───
  window.updateCartItem = function (key, quantity) {
    fetch('/carrinho/atualizar/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrf(),
      },
      body: JSON.stringify({ key, quantity }),
    })
    .then(r => r.json())
    .then(data => {
      if (data.success) {
        updateCartBadge(data.cart_count);
        reloadCartDrawer();
      }
    });
  };

  // ─── REMOVE FROM CART ───
  window.removeCartItem = function (key) {
    const item = document.querySelector(`.cart-item[data-key="${key}"]`);
    if (item) {
      item.style.transition = 'all 0.3s ease';
      item.style.opacity = '0';
      item.style.transform = 'translateX(20px)';
    }

    setTimeout(() => {
      fetch('/carrinho/remover/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrf(),
        },
        body: JSON.stringify({ key }),
      })
      .then(r => r.json())
      .then(data => {
        if (data.success) {
          updateCartBadge(data.cart_count);
          reloadCartDrawer();
        }
      });
    }, 300);
  };

  // ─── RELOAD CART DRAWER ───
  function reloadCartDrawer() {
    // Simple page reload to update the cart drawer
    // In production, this should be an AJAX call to a partial view
    window.location.reload();
  }

  // ─── ADD TO CART BUTTON ON PRODUCT PAGE ───
  const addToCartForm = document.getElementById('add-to-cart-form');
  if (addToCartForm) {
    addToCartForm.addEventListener('submit', function (e) {
      e.preventDefault();
      const formData = new FormData(this);
      const productId = formData.get('product_id');
      const variantId = formData.get('variant_id');
      const quantity = parseInt(formData.get('quantity') || '1');

      if (!variantId) {
        showNotification('Por favor, selecione uma cor e tamanho.', 'error');
        return;
      }

      const btn = this.querySelector('[type="submit"]');
      const originalText = btn.textContent;
      btn.textContent = 'Adicionando...';
      btn.disabled = true;

      addToCart(productId, variantId, quantity)
        .then(() => {
          btn.textContent = '✓ Adicionado!';
          btn.style.background = 'var(--success)';
          setTimeout(() => {
            btn.textContent = originalText;
            btn.style.background = '';
            btn.disabled = false;
          }, 2500);
          openCartDrawer();
        });
    });
  }

});
