// Pricing Toggle Functionality
document.addEventListener('DOMContentLoaded', () => {
  const plans = [
    {
      name: 'Plan Base',
      prices: { monthly: 'GRATIS', yearly: 'GRATIS' }, ids: { monthly: 0, yearly: 0 },
      intro:'de por vida',
      features: [
        { label: '<br></br>🍽️ Menu Online', info: 'Actualizá tu carta en tiempo real' },
        { label: '🔄 Actualizaciones', info: 'Actualizá tu carta en tiempo real' },
        { label: '📱Diseño Responsivo', info: 'Compatible con móviles y tablets' },
        { label: '🍝 Hasta 25 Ítems', info: 'Podés cargar hasta 25 ítems en tu carta' },
        { label: '🏪 Data Negocio', info: 'Dirección, horarios de atencion, etc' },
        { label: '🔐 Sitio Seguro SSL', info: 'Certificado SSL incluido' }
      ]
    },
    {
      name: 'Plan Emprendedor',
      prices: { monthly: '$18.000', yearly: '$180.000' }, ids: { monthly: 1, yearly: 4 },
      intro:'todo lo anterior, más:',
      features: [
        { label: '<br></br>🤳 Código QR', info: 'Código QR único para tu carta' },
        { label: '🪧 Sin Publicidad', info: 'Carta sin banners ni anuncios externos' },
        { label: '🛏️ Hosting 24/7', info: 'Acceso permanente a la carta online' },
        { label: '🍝 Ítems Ilimitados', info: 'Sin límite de carga de ítems' },
        { label: '🔎 Búsqueda de Platos', info: 'Buscar rápidamente platos dentro de tu carta digital' },
        { label: '📞 Atención Virtual', info: 'Tiempo de respuesta en menos de 72h' },
        { label: '<div style="text-align:center;"><b><br></br>EXTRA</b></div>' },
        { label: '<div style="text-align:center;">✅5%OFF en <a href="#productos" style="color:#1976d2;text-decoration:underline;cursor:pointer;">Productos</a></div>', modes: ['monthly']},
        { label: '<div style="text-align:center;">✅<b>10%OFF</b> en <a href="#productos" style="color:#1976d2;text-decoration:underline;cursor:pointer;">Productos</a></div>', modes: ['yearly']}
      ]
    },
    {
      name: 'Plan Profesional',
      prices: { monthly: '$36.000', yearly: '$360.000' }, ids: { monthly: 2, yearly: 5 },
      intro:'Todo lo anterior, más:',
      features: [
        { label: '<br></br>💬 Integración WhatsApp', info: 'Contacto directo vía WhatsApp' },
        { label: '🛵 Integración Rappi/PedidosYa', info: 'Enlaces a aplicaciones de delivery' },
        { label: '🗣️ Integración Instagram/Facebook', info: 'Enlaces a redes sociales desde tu carta' },
        { label: '📍 Integración Google Maps', info: 'Enlace con dirección de tu negocio' },
        { label: '🎨 Tema Personalizable', info: 'Elegí tipo de letra y paleta de colores' },
        { label: '📞 Atención Personalizada', info: 'Tiempo de respuesta en menos de 42h' },
        { label: '<div style="text-align:center;"><b><br></br>EXTRA</b></div>' },
        { label: '<div style="text-align:center;">✅10%OFF en <a href="#productos" style="color:#1976d2;text-decoration:underline;cursor:pointer;">Productos</a></div>', modes: ['monthly']},
        { label: '<div style="text-align:center;">✅<b>20%OFF</b> en <a href="#productos" style="color:#1976d2;text-decoration:underline;cursor:pointer;">Productos</a></div>', modes: ['yearly']}
      ]
    },
    {
      name: 'Plan Corporativo',
      prices: { monthly: '$72.000', yearly: '$720.000' }, ids: { monthly: 3, yearly: 6 },
      intro:'todo lo anterior, más:',
      features: [
        { label: '<br></br>📷 Fotos de Platos', info: 'Galería fotográfica para mostrar tus productos' },
        { label: '🛍️ Promos por Temporada', info: 'Mensajes pop up promocionales' },
        { label: '🛒 Pedidos por web', info: 'Permití que tus clientes hagan pedidos directamente desde la carta online' },
        { label: '🌐 Dominio Propio', info: 'URL personalizable www.tunegocio.com.ar' },
        { label: '📞 Atención Prioritaria', info: 'Tiempo de respuesta en menos de 24h' },
        { label: '<div style="text-align:center;"><b><br></br>EXTRA</b></div>' },
        { label: '<div style="text-align:center;">✅15%OFF en <a href="#productos" style="color:#1976d2;text-decoration:underline;cursor:pointer;">Productos</a></div>', modes: ['monthly']},
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
  
  
  // General button handlers
  document.querySelectorAll('.navbar8-action11, .navbar8-action21, .hero17-button1, .hero17-button2').forEach(button => {
    button.addEventListener('click', function() {
      const text = this.textContent.trim();
      alert(`Botón "${text}" clickeado - Agrega aquí la funcionalidad deseada`);
    });
  });
  
  // Mobile menu handlers
  document.querySelector('.navbar8-burger-menu').addEventListener('click', function() {
    const mobileMenu = document.querySelector('.navbar8-mobile-menu');
    mobileMenu.style.display = mobileMenu.style.display === 'block' ? 'none' : 'block';
  });
  
  document.querySelector('.navbar8-close-menu').addEventListener('click', function() {
    document.querySelector('.navbar8-mobile-menu').style.display = 'none';
  });
  
  // Debugging all buttons
  document.querySelectorAll('button, a').forEach(element => {
    element.addEventListener('click', function(e) {
      console.log('Elemento clickeado:', this);
    });
  });
    
  const burger = document.querySelector('[data-thq="thq-burger-menu"]');
  const mobileMenu = document.querySelector('[data-thq="thq-mobile-menu"]');
  const closeMenu = document.querySelector('[data-thq="thq-close-menu"]');
  
  if (burger && mobileMenu && closeMenu) {
    burger.addEventListener("click", () => {
      mobileMenu.classList.add("active");
    });
    
    closeMenu.addEventListener("click", () => {
      mobileMenu.classList.remove("active");
    });
  }
  
  // Verificar específicamente los botones de pricing
  const monthlyBtn = document.getElementById('monthlyBtn');
  const yearlyBtn = document.getElementById('yearlyBtn');
  
  if (monthlyBtn) {
    monthlyBtn.addEventListener('click', function() {
      console.log('Monthly button clicked');
    });
  }
  
  if (yearlyBtn) {
    yearlyBtn.addEventListener('click', function() {
      console.log('Yearly button clicked');
    });
  }
  // Cargar fechas ocupadas desde el endpoint
  let fechasOcupadas = [];
  
  // 1. Referencia al botón
  const btn2 = document.getElementById('btnReserva');
  
  // 2. Asegurarse de que el botón existe
  if (!btn2) {
    console.warn("⚠️ No se encontró el botón #btnReserva");
    return;
  } else {
    btn2.addEventListener('click', (e) => {
      e.preventDefault();
      // 3. Cargar fechas ocupadas y guardar en variable
      fetch('https://script.google.com/macros/s/AKfycbxgKDs5ImPgPyOh0vrh5RAeM2tyttFGkFR_sheDK_cZU0l1Q_9R9nkY6lmLmb8igxMq/exec')
        .then(res => res.json())
        .then(data => {
          console.log("📅 Fechas ocupadas:", fechasOcupadas);
          localStorage.setItem('fechasOcupadas', JSON.stringify(data));
          window.location.href = "reserva.html";
        })
        .catch(err => {
        console.error("❌ Error al cargar fechas ocupadas:", err);
        // Navega igual aunque falle el fetch
        window.location.href = "reserva.html";
        });
      })
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
  document.getElementById('cart-count').textContent = getCart().length;
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


// Cierra el menú al hacer clic en cualquier enlace
document.querySelectorAll('#mobileMenu a').forEach(link => {
  link.addEventListener('click', function() {
    document.getElementById('mobileMenu').classList.remove('open');
  });
}
);

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
