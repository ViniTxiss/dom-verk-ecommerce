// DOM VERK — animations.js
document.addEventListener('DOMContentLoaded', () => {

  // ─── AOS INIT ───
  if (typeof AOS !== 'undefined') {
    AOS.init({
      duration: 700,
      easing: 'ease-out-cubic',
      once: true,
      offset: 60,
    });
  }

  // ─── GSAP TICKER (fallback if GSAP not loaded) ───
  if (typeof gsap !== 'undefined') {
    // Slow hero parallax on scroll
    const heroImg = document.querySelector('.hero__img');
    if (heroImg) {
      window.addEventListener('scroll', () => {
        const scrolled = window.scrollY;
        gsap.to(heroImg, {
          y: scrolled * 0.25,
          duration: 0,
          overwrite: true,
        });
      }, { passive: true });
    }

    // Stagger product cards on load
    const productCards = document.querySelectorAll('.product-card');
    if (productCards.length > 0) {
      gsap.fromTo(productCards,
        { opacity: 0, y: 30 },
        {
          opacity: 1,
          y: 0,
          duration: 0.5,
          stagger: 0.08,
          ease: 'power2.out',
          delay: 0.2,
        }
      );
    }
  }

  // ─── SCROLL LINE HERO ───
  const scrollLine = document.querySelector('.scroll-line');
  if (scrollLine) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 100) {
        scrollLine.style.opacity = '0';
      } else {
        scrollLine.style.opacity = '1';
      }
    }, { passive: true });
  }

  // ─── PRODUCT IMAGE HOVER ───
  document.querySelectorAll('.product-card__img-wrap').forEach(wrap => {
    const primaryImg = wrap.querySelector('.product-card__img:not(.product-card__img--hover)');
    const hoverImg = wrap.querySelector('.product-card__img--hover');

    if (primaryImg && hoverImg) {
      wrap.addEventListener('mouseenter', () => {
        primaryImg.style.opacity = '0';
        hoverImg.style.opacity = '1';
      });
      wrap.addEventListener('mouseleave', () => {
        primaryImg.style.opacity = '1';
        hoverImg.style.opacity = '0';
      });
    }
  });

  // ─── VARIANT SELECTOR ───
  const colorBtns = document.querySelectorAll('[data-color]');
  const sizeBtns = document.querySelectorAll('[data-size-btn]');
  const variantInput = document.getElementById('variant-id-input');

  function updateVariantInput() {
    const selectedColor = document.querySelector('[data-color].selected')?.dataset.color;
    const selectedSize = document.querySelector('[data-size-btn].selected')?.dataset.sizeBtn;

    if (selectedColor && selectedSize && variantInput) {
      // Find variant ID from data attributes
      const variantData = document.querySelectorAll('[data-variant]');
      for (const v of variantData) {
        if (v.dataset.color === selectedColor && v.dataset.size === selectedSize) {
          variantInput.value = v.dataset.variantId;
          break;
        }
      }
    }
  }

  colorBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      colorBtns.forEach(b => b.classList.remove('selected'));
      btn.classList.add('selected');
      updateVariantInput();
    });
  });

  sizeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      sizeBtns.forEach(b => b.classList.remove('selected'));
      btn.classList.add('selected');
      updateVariantInput();
    });
  });

  // ─── SMOOTH SCROLL TO ANCHOR ───
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href');
      const target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // ─── SCALEPOP ANIMATION (for cart badge) ───
  const style = document.createElement('style');
  style.textContent = `
    @keyframes scalePop {
      0% { transform: scale(1); }
      50% { transform: scale(1.4); }
      100% { transform: scale(1); }
    }
  `;
  document.head.appendChild(style);

  // ─── GALLERY LIGHTBOX (Product Detail) ───
  const galleryThumbs = document.querySelectorAll('.gallery-thumb');
  const galleryMain = document.getElementById('gallery-main');

  galleryThumbs.forEach(thumb => {
    thumb.addEventListener('click', () => {
      if (galleryMain) {
        galleryMain.src = thumb.src;
        galleryMain.style.animation = 'none';
        galleryMain.offsetHeight;
        galleryMain.style.animation = 'fadeIn 0.3s ease';
      }
      galleryThumbs.forEach(t => t.classList.remove('active'));
      thumb.classList.add('active');
    });
  });

});
