// Pricing Toggle Functionality
document.addEventListener('DOMContentLoaded', () => {
  const plans = [
    {
      name: 'Plan Base',
      prices: { monthly: 'GRATIS', yearly: 'GRATIS' }, ids: { monthly: 0, yearly: 0 },
      intro:'de por vida',
      features: [
        { label: '<br></br>🍽️ Menu Online', info: 'Tené ya mismo tu Menú online' },
        { label: '🔄 Actualizaciones', info: 'Actualizá tu menú en tiempo real' },
        { label: '📱Diseño Responsivo', info: 'Compatible con móviles y tablets' },
        { label: '🍝 Hasta 25 Ítems', info: 'Podés cargar hasta 25 ítems en tu menú' },
        { label: '🏪 Data Negocio', info: 'Dirección, horarios de atencion, etc' }
      ]
    },
    {
      name: 'Plan Emprendedor',
      prices: { monthly: '$15.000', yearly: '$150.000' }, ids: { monthly: 1, yearly: 4 },
      intro:'Editá e imprimí tu menú en segundos',
      features: [
        { label: '<br></br>📖 Menú Imprimible', info: 'Generá un archivo listo para imprimir al instante' },
        { label: '✏️ Edición Completa', info: 'Modificá tu menú directamente en Google Sheets' },
        { label: '🎨 Paleta Personalizable', info: 'Adaptá tu menú a los colores de tu marca' },
        { label: '➕ Ítems Ilimitados', info: 'Agregá todos los platos que necesites' },
        { label: '🪧 Sin Publicidad', info: 'Menú sin banners ni anuncios externos' },
        { label: '<div style="text-align:center;"><b><br></br></b></div>' },
        { label: '<div style="text-align:center;">✅<b>5%OFF</b> en <a href="#productos" style="color:#1976d2;text-decoration:underline;cursor:pointer;">Productos</a></div>', modes: ['monthly']},
        { label: '<div style="text-align:center;">✅<b>10%OFF</b> en <a href="#productos" style="color:#1976d2;text-decoration:underline;cursor:pointer;">Productos</a></div>', modes: ['yearly']}
      ]
    },
    {
      name: 'Plan Profesional',
      prices: { monthly: '$30.000', yearly: '$300.000' }, ids: { monthly: 2, yearly: 5 },
      intro:'Todo lo anterior, más:',
      features: [
        { label: '<br></br>🪄 Menú Imprimible + Online', info: 'Carta digital y lista para imprimir' },
        { label: '🤳 Código QR', info: 'Generá un QR único para tu menú' },
        { label: '📲 Redes Sociales', info: 'Enlaces a WhatsApp, Instagram, Facebook y GMaps' },
        { label: '🛵 Apps de Delivery', info: 'Conectá tu negocio a PedidosYa y Rappi' },
        { label: '🌍 Traducción a varios idiomas', info: 'Tu menú disponible en varios idiomas' },
        { label: '<div style="text-align:center;"><b><br></br></b></div>' },
        { label: '<div style="text-align:center;">✅<b>10%OFF</b> en <a href="#productos" style="color:#1976d2;text-decoration:underline;cursor:pointer;">Productos</a></div>', modes: ['monthly']},
        { label: '<div style="text-align:center;">✅<b>20%OFF</b> en <a href="#productos" style="color:#1976d2;text-decoration:underline;cursor:pointer;">Productos</a></div>', modes: ['yearly']}
      ]
    },
    {
      name: 'Plan Corporativo',
      prices: { monthly: '$45.000', yearly: '$450.000' }, ids: { monthly: 3, yearly: 6 },
      intro:'Todo lo anterior, más:',
      features: [
        { label: '<br></br>📷 Integración de Fotos', info: 'Integración de galería fotográfica para mostrar tus productos' },
        { label: '🛍️ Promos por Temporada', info: 'Mensajes promocionales' },
        { label: '📅 Integración de Reservas', info: 'Reservas a través de GForms' },
        { label: '🛒 Pedidos por Web', info: 'Pedidos desde tu menú online' },
        { label: '📞 Atención Prioritaria', info: 'Tiempo de respuesta en menos de 24h' },
        { label: '<div style="text-align:center;"><b><br></br></b></div>' },
        { label: '<div style="text-align:center;">✅<b>15%OFF</b> en <a href="#productos" style="color:#1976d2;text-decoration:underline;cursor:pointer;">Productos</a></div>', modes: ['monthly']},
        { label: '<div style="text-align:center;">✅<b>30%OFF</b> en <a href="#productos" style="color:#1976d2;text-decoration:underline;cursor:pointer;">Productos</a></div>', modes: ['yearly']}
      ]
    }
  ];

  let currentMode = 'monthly';
  
  function togglePricing(mode) {
    currentMode = mode;
    document.querySelectorAll('.pricing-toggle button').forEach(btn => {
      btn.classList.remove('active');
    });
    document.getElementById(`${mode}Btn`).classList.add('active');
    renderPricing(mode);
  }
  
  function renderPricing(mode) {
    const container = document.getElementById('pricingContainer');
    container.innerHTML = '';
    
    plans.forEach(plan => {
      const card = document.createElement('div');
      card.className = 'pricing-card';
      
      const planId = plan.ids[mode];
      
      card.innerHTML = `
      <h3>${plan.name}</h3>
      <div class="price">${plan.prices[mode]}</div>
      ${plan.intro ? `<div class="plan-intro">${plan.intro}</div>` : ''}
      <ul class="feature-list">
        ${plan.features
          .filter(f => !f.modes || f.modes.includes(mode))
          .map(f => `
            <li>
            ${f.label}
            ${(!f.label.includes('EXTRA') && f.info) ? `<span class="info-icon" tabindex="0" data-tooltip="${f.info}">i</span>` : ''}                        
            </li>
            `).join('')}
      </ul>
      <div style="margin-bottom: 4px;" >
        <button class="select-btn demo-btn" data-plan="${planId}" data-demo="${plan.name.toLowerCase().includes('base') ? 'base' : plan.name.toLowerCase().includes('emprendedor') ? 'emprendedor' : plan.name.toLowerCase().includes('profesional') ? 'profesional' : 'corporativo'}">Demo</button>
      </div>
      <button class="select-btn" data-plan="${planId}">Seleccionar</button>
      `;
      
      container.appendChild(card);
    });
    
    // Agregar redirección a todos los botones
    document.querySelectorAll('.select-btn').forEach(btn => {
      if (btn.classList.contains('demo-btn')) {
        btn.addEventListener('click', (e) => {
          const demoType = e.currentTarget.getAttribute('data-demo');
          window.open(`demo/${demoType}.html`, '_blank');
        });
      } else {
        btn.addEventListener('click', (e) => {
          const planId = e.currentTarget.getAttribute('data-plan');
          window.location.href = `plansForm.html?plan=${planId}`;
        });
      }
    });
  }
  
  document.getElementById('monthlyBtn').addEventListener('click', () => togglePricing('monthly'));
  document.getElementById('yearlyBtn').addEventListener('click', () => togglePricing('yearly'));
  
  togglePricing('monthly');

  // Mobile menu
  const burger = document.querySelector('[data-thq="thq-burger-menu"]');
  const mobileMenu = document.querySelector('[data-thq="thq-mobile-menu"]');
  const closeBtn = document.querySelector('[data-thq="thq-close-menu"]');

  burger.addEventListener('click', () => {
    mobileMenu.classList.add('open');
  });

  closeBtn.addEventListener('click', () => {
    mobileMenu.classList.remove('open');
  });

  // Cerrar menú si se hace clic fuera
  document.addEventListener('click', (e) => {
    if (mobileMenu.classList.contains('open') &&
        !mobileMenu.contains(e.target) &&
        !burger.contains(e.target)) {
      mobileMenu.classList.remove('open');
    }
  });

  // Cerrar al hacer clic en un link
  mobileMenu.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      mobileMenu.classList.remove('open');
    });
  });

  
  // Cargar fechas ocupadas desde el endpoint
  // Referencia al botón de reservas
  const btn2 = document.getElementById('btnReserva');
  const loader = document.getElementById('noPayLoader');

  if (btn2) {
    btn2.addEventListener('click', (e) => {
      e.preventDefault();
      if (loader) loader.style.display = 'inline-block';
      fetch('https://script.google.com/macros/s/AKfycbwuJtQJxCthv-prpaGWYAK-Gp6iibmwbMsjyicufZjqj8vDqbpULkDj7sVoCrgCiJ-x/exec')
        .then(res => res.json())
        .then(data => {
          localStorage.setItem('fechasOcupadas', JSON.stringify(data));
          window.location.href = 'reserva.html';
        })
        .catch(() => {
          // Navega igual aunque falle el fetch
          window.location.href = 'reserva.html';
        });
    });
  }
});

// Inicializar carrito desde localStorage
function getCart() {
  return JSON.parse(localStorage.getItem('cart') || '[]');
}
function setCart(cart) {
  localStorage.setItem('cart', JSON.stringify(cart));
}
function updateCartCount() {
  const count = getCart().length;
  document.getElementById('cart-count').textContent = count;
  const checkoutBtn = document.getElementById('cartCheckoutBtn');
  if (checkoutBtn) checkoutBtn.style.display = count > 0 ? 'inline-block' : 'none';
}

// Al cargar la página, marcar los checkboxes ya seleccionados
updateCartCount();
const cart = getCart();
document.querySelectorAll('.cart-checkbox').forEach(checkbox => {
  if (cart.includes(checkbox.dataset.product)) {
    checkbox.checked = true;
  }
  checkbox.addEventListener('change', function() {
    let cart = getCart();
    if (this.checked) {
      if (!cart.includes(this.dataset.product)) cart.push(this.dataset.product);
    } else {
      cart = cart.filter(p => p !== this.dataset.product);
    }
    setCart(cart);
    updateCartCount();
  });
});




  let activeCategory = 'Sitio Web'; // inicial
  
  function filterCategory(category) {
    const cards = document.querySelectorAll('.product-card');
    const buttons = document.querySelectorAll('.toggle-button');
    
    // Si el usuario hace clic en el mismo botón activo, lo desactiva
    if (activeCategory === category) {
      activeCategory = null;
      buttons.forEach(btn => btn.classList.remove('active'));
      cards.forEach(card => card.style.display = 'block');
      return;
    }
    
    // Si hace clic en una nueva categoría
    activeCategory = category;
    buttons.forEach(btn => {
      btn.classList.toggle('active', btn.textContent === category);
    });
    
    cards.forEach(card => {
      const cat = card.querySelector('.product-category').textContent;
      card.style.display = (cat === category) ? 'block' : 'none';
    });
  }

// ── Scroll-reveal animation ─────────────────────────
(function initReveal() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.05 });
  document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
})();

// ── Scroll-spy navbar active link ───────────────────
(function initScrollSpy() {
  const sections = document.querySelectorAll('section[id], div[id]');
  const navLinks = document.querySelectorAll('.navbar8-links a');
  if (!navLinks.length) return;

  const spy = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const id = entry.target.id;
      navLinks.forEach(a => {
        a.classList.toggle('nav-active', a.getAttribute('href') === `#${id}`);
      });
    });
  }, { rootMargin: '-40% 0px -55% 0px' });

  sections.forEach(s => spy.observe(s));
})();