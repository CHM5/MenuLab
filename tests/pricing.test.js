/**
 * Unit tests — Pricing toggle (script.js)
 * Probamos la lógica de renderPricing y togglePricing con un DOM mínimo.
 */

// ─── datos y funciones extraídas de script.js ─────────────────────────────────
const plans = [
  {
    name: 'Plan Base',
    prices: { monthly: 'GRATIS', yearly: 'GRATIS' },
    ids: { monthly: 0, yearly: 0 },
    intro: 'de por vida',
    features: [
      { label: '🍽️ Menu Online', info: 'Tené ya mismo tu Menú online' },
      { label: '🔄 Actualizaciones', info: 'Actualizá tu menú en tiempo real' },
    ],
  },
  {
    name: 'Plan Emprendedor',
    prices: { monthly: '$15.000', yearly: '$150.000' },
    ids: { monthly: 1, yearly: 4 },
    intro: 'Editá e imprimí tu menú en segundos',
    features: [
      { label: '📖 Menú Imprimible', info: 'Generá un archivo listo para imprimir' },
      { label: '✅<b>5%OFF</b>', modes: ['monthly'] },
      { label: '✅<b>10%OFF</b>', modes: ['yearly'] },
    ],
  },
  {
    name: 'Plan Profesional',
    prices: { monthly: '$30.000', yearly: '$300.000' },
    ids: { monthly: 2, yearly: 5 },
    intro: 'Todo lo anterior, más:',
    features: [
      { label: '🤳 Código QR', info: 'Generá un QR único para tu menú' },
      { label: '✅<b>10%OFF</b>', modes: ['monthly'] },
      { label: '✅<b>20%OFF</b>', modes: ['yearly'] },
    ],
  },
  {
    name: 'Plan Corporativo',
    prices: { monthly: '$45.000', yearly: '$450.000' },
    ids: { monthly: 3, yearly: 6 },
    intro: 'Todo lo anterior, más:',
    features: [
      { label: '📷 Integración de Fotos', info: 'Galería fotográfica' },
      { label: '✅<b>15%OFF</b>', modes: ['monthly'] },
      { label: '✅<b>30%OFF</b>', modes: ['yearly'] },
    ],
  },
];

function renderPricing(mode, container) {
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
          .map(f => `<li>${f.label}${f.info ? `<span class="info-icon" data-tooltip="${f.info}">i</span>` : ''}</li>`)
          .join('')}
      </ul>
      <button class="select-btn demo-btn" data-plan="${planId}" data-demo="${
        plan.name.toLowerCase().includes('base') ? 'base'
        : plan.name.toLowerCase().includes('emprendedor') ? 'emprendedor'
        : plan.name.toLowerCase().includes('profesional') ? 'profesional'
        : 'corporativo'
      }">Demo</button>
      <button class="select-btn" data-plan="${planId}">Seleccionar</button>
    `;
    container.appendChild(card);
  });
}

// ─────────────────────────────────────────────────────────────────────────────

describe('renderPricing — modo mensual', () => {
  let container;

  beforeEach(() => {
    container = document.createElement('div');
    renderPricing('monthly', container);
  });

  test('renderiza 4 tarjetas', () => {
    expect(container.querySelectorAll('.pricing-card').length).toBe(4);
  });

  test('Plan Base muestra precio GRATIS', () => {
    expect(container.querySelector('.pricing-card .price').textContent).toBe('GRATIS');
  });

  test('Plan Emprendedor muestra descuento mensual (5%OFF), no anual (10%OFF)', () => {
    const cards = container.querySelectorAll('.pricing-card');
    const empCard = cards[1];
    expect(empCard.innerHTML).toContain('5%OFF');
    expect(empCard.innerHTML).not.toContain('10%OFF');
  });

  test('botón Seleccionar del Plan Emprendedor tiene data-plan="1"', () => {
    const cards = container.querySelectorAll('.pricing-card');
    const empCard = cards[1];
    const btn = empCard.querySelector('.select-btn:not(.demo-btn)');
    expect(btn.getAttribute('data-plan')).toBe('1');
  });

  test('botón Demo del Plan Corporativo tiene data-demo="corporativo"', () => {
    const cards = container.querySelectorAll('.pricing-card');
    const corpCard = cards[3];
    const btn = corpCard.querySelector('.demo-btn');
    expect(btn.getAttribute('data-demo')).toBe('corporativo');
  });

  test('todos los planes tienen el intro visible', () => {
    const intros = container.querySelectorAll('.plan-intro');
    expect(intros.length).toBe(4);
  });
});

describe('renderPricing — modo anual', () => {
  let container;

  beforeEach(() => {
    container = document.createElement('div');
    renderPricing('yearly', container);
  });

  test('Plan Emprendedor muestra descuento anual (10%OFF), no mensual (5%OFF)', () => {
    const cards = container.querySelectorAll('.pricing-card');
    const empCard = cards[1];
    expect(empCard.innerHTML).toContain('10%OFF');
    expect(empCard.innerHTML).not.toContain('5%OFF');
  });

  test('Plan Corporativo muestra 30%OFF en modo anual', () => {
    const cards = container.querySelectorAll('.pricing-card');
    const corpCard = cards[3];
    expect(corpCard.innerHTML).toContain('30%OFF');
  });

  test('botón Seleccionar del Plan Emprendedor tiene data-plan="4" (anual)', () => {
    const cards = container.querySelectorAll('.pricing-card');
    const empCard = cards[1];
    const btn = empCard.querySelector('.select-btn:not(.demo-btn)');
    expect(btn.getAttribute('data-plan')).toBe('4');
  });

  test('Plan Profesional tiene precio $300.000 en modo anual', () => {
    const cards = container.querySelectorAll('.pricing-card');
    const proCard = cards[2];
    expect(proCard.querySelector('.price').textContent).toBe('$300.000');
  });
});

describe('togglePricing (DOM completo)', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <div class="pricing-toggle">
        <button id="monthlyBtn">Mensual</button>
        <button id="yearlyBtn">Anual</button>
      </div>
      <div id="pricingContainer"></div>
    `;
  });

  function togglePricing(mode) {
    document.querySelectorAll('.pricing-toggle button').forEach(btn => btn.classList.remove('active'));
    document.getElementById(`${mode}Btn`).classList.add('active');
    renderPricing(mode, document.getElementById('pricingContainer'));
  }

  test('al activar mensual, el botón mensual tiene clase active', () => {
    togglePricing('monthly');
    expect(document.getElementById('monthlyBtn').classList.contains('active')).toBe(true);
    expect(document.getElementById('yearlyBtn').classList.contains('active')).toBe(false);
  });

  test('al activar anual, el botón anual tiene clase active', () => {
    togglePricing('yearly');
    expect(document.getElementById('yearlyBtn').classList.contains('active')).toBe(true);
    expect(document.getElementById('monthlyBtn').classList.contains('active')).toBe(false);
  });

  test('cambiar de mensual a anual actualiza los precios en el DOM', () => {
    togglePricing('monthly');
    const beforePrice = document.querySelectorAll('.pricing-card')[1].querySelector('.price').textContent;

    togglePricing('yearly');
    const afterPrice = document.querySelectorAll('.pricing-card')[1].querySelector('.price').textContent;

    expect(beforePrice).toBe('$15.000');
    expect(afterPrice).toBe('$150.000');
  });
});
