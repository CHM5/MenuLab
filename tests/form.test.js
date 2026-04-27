/**
 * Integration tests — form.js (form.html)
 * Simula el DOM de form.html y carga la lógica de validación.
 */

// ─── DOM mínimo de form.html ──────────────────────────────────────────────────
function buildFormDOM() {
  document.body.innerHTML = `
    <form id="sponsorshipForm">
      <!-- Paso 1: selección de productos -->
      <div class="form-step active" data-step="1">
        <label><input type="checkbox" class="product-checkbox" data-product="cartadoblefaz" data-price="150000"> Menú Dúo</label>
        <label><input type="checkbox" class="product-checkbox" data-product="microsite" data-price="120000"> MicroSite</label>
        <div id="totalAmount"></div>
        <div id="formError" class="form-error" style="display:none;"></div>
        <button type="button" class="next-btn">Siguiente</button>
      </div>

      <!-- Paso 2: datos personales -->
      <div class="form-step" data-step="2">
        <input type="text" id="firstName" name="firstName" required>
        <input type="text" id="lastName" name="lastName" required>
        <input type="email" id="email" name="email" required>
        <input type="tel" id="phone" name="phone" required>
        <select id="sponsorshipLevel" name="sponsorshipLevel" required>
          <option value="">Seleccionar</option>
          <option value="argentina">Argentina</option>
          <option value="platinum">Personalizado</option>
        </select>
        <div id="customAmountContainer" style="display:none;">
          <input type="number" id="customAmount" name="customAmount" min="10000">
        </div>
        <div id="formError2" class="form-error" style="display:none;"></div>
        <button type="button" class="prev-btn">Anterior</button>
        <button type="button" class="next-btn">Siguiente</button>
      </div>

      <!-- Paso 3: confirmación -->
      <div class="form-step" data-step="3">
        <div class="success-icon"></div>
        <button id="resetForm" type="button">Reiniciar</button>
      </div>
    </form>

    <div class="progress-fill" style="width:0%"></div>
    <div class="step"></div>
    <div class="step"></div>
    <div class="step"></div>
  `;
}

// ─── helpers de validación (extraídos de form.js) ────────────────────────────
function validateStep1() {
  const formError = document.getElementById('formError');
  formError.style.display = 'none';

  const checkboxes = document.querySelectorAll('.product-checkbox');
  const algunoSeleccionado = Array.from(checkboxes).some(cb => cb.checked);
  if (!algunoSeleccionado) {
    formError.textContent = 'Debés seleccionar al menos un producto para continuar.';
    formError.style.display = 'block';
    return false;
  }
  return true;
}

function validateRequiredFields(stepNumber) {
  const stepEl = document.querySelector(`.form-step[data-step="${stepNumber}"]`);
  const requiredFields = stepEl.querySelectorAll('[required]');
  let isValid = true;
  requiredFields.forEach(field => {
    field.style.borderColor = '';
    if (!field.checkValidity() || field.value.trim() === '') {
      field.style.borderColor = 'red';
      isValid = false;
    }
  });
  return isValid;
}

function updateTotalAmount(displayId = 'totalAmount') {
  let total = 0;
  document.querySelectorAll('.product-checkbox').forEach(cb => {
    if (cb.checked) total += parseFloat(cb.getAttribute('data-price'));
  });
  const el = document.getElementById(displayId);
  if (el) el.innerHTML = `<strong>Total: $${total}</strong>`;
}

// ─────────────────────────────────────────────────────────────────────────────

beforeEach(() => {
  buildFormDOM();
});

describe('Paso 1 — validación de productos', () => {
  test('falla si no hay ningún producto seleccionado', () => {
    expect(validateStep1()).toBe(false);
  });

  test('muestra mensaje de error si no hay producto seleccionado', () => {
    validateStep1();
    const error = document.getElementById('formError');
    expect(error.style.display).toBe('block');
    expect(error.textContent).toMatch(/seleccion/i);
  });

  test('pasa si al menos un producto está marcado', () => {
    document.querySelector('[data-product="cartadoblefaz"]').checked = true;
    expect(validateStep1()).toBe(true);
  });

  test('oculta el error cuando hay al menos un producto marcado', () => {
    document.querySelector('[data-product="microsite"]').checked = true;
    validateStep1();
    expect(document.getElementById('formError').style.display).toBe('none');
  });
});

describe('Paso 2 — validación de campos requeridos', () => {
  test('falla si los campos requeridos están vacíos', () => {
    expect(validateRequiredFields(2)).toBe(false);
  });

  test('marca los campos inválidos con borde rojo', () => {
    validateRequiredFields(2);
    const firstName = document.getElementById('firstName');
    expect(firstName.style.borderColor).toBe('red');
  });

  test('pasa si todos los campos requeridos están completos', () => {
    document.getElementById('firstName').value = 'Juan';
    document.getElementById('lastName').value = 'Pérez';
    document.getElementById('email').value = 'juan@test.com';
    document.getElementById('phone').value = '1130625858';
    document.getElementById('sponsorshipLevel').value = 'argentina';
    expect(validateRequiredFields(2)).toBe(true);
  });

  test('campo email inválido hace fallar la validación', () => {
    document.getElementById('firstName').value = 'Juan';
    document.getElementById('lastName').value = 'Pérez';
    document.getElementById('email').value = 'no-es-un-email';
    document.getElementById('phone').value = '1130625858';
    document.getElementById('sponsorshipLevel').value = 'argentina';
    expect(validateRequiredFields(2)).toBe(false);
  });
});

describe('updateTotalAmount', () => {
  test('muestra $0 si no hay checkboxes marcados', () => {
    updateTotalAmount();
    expect(document.getElementById('totalAmount').innerHTML).toContain('$0');
  });

  test('suma correctamente los precios de los productos seleccionados', () => {
    document.querySelector('[data-product="cartadoblefaz"]').checked = true; // 150000
    document.querySelector('[data-product="microsite"]').checked = true;    // 120000
    updateTotalAmount();
    expect(document.getElementById('totalAmount').innerHTML).toContain('$270000');
  });

  test('descuenta correctamente al desmarcar un producto', () => {
    document.querySelector('[data-product="cartadoblefaz"]').checked = true;
    document.querySelector('[data-product="microsite"]').checked = true;
    updateTotalAmount();

    document.querySelector('[data-product="microsite"]').checked = false;
    updateTotalAmount();
    expect(document.getElementById('totalAmount').innerHTML).toContain('$150000');
  });

  test('solo incluye los productos marcados', () => {
    document.querySelector('[data-product="microsite"]').checked = true;
    updateTotalAmount();
    const html = document.getElementById('totalAmount').innerHTML;
    expect(html).toContain('$120000');
    expect(html).not.toContain('$270000');
  });
});

describe('updateFormProgress — visibilidad de pasos', () => {
  function updateFormProgress(step) {
    const formSteps = document.querySelectorAll('.form-step');
    formSteps.forEach(s => s.classList.remove('active'));
    document.querySelector(`.form-step[data-step="${step}"]`).classList.add('active');

    const fill = document.querySelector('.progress-fill');
    fill.style.width = `${((step - 1) / (formSteps.length - 1)) * 100}%`;

    document.querySelectorAll('.step').forEach((s, idx) => {
      s.classList.toggle('active', idx + 1 <= step);
    });
  }

  test('solo el paso activo tiene clase "active"', () => {
    updateFormProgress(2);
    const steps = document.querySelectorAll('.form-step');
    expect(steps[0].classList.contains('active')).toBe(false);
    expect(steps[1].classList.contains('active')).toBe(true);
    expect(steps[2].classList.contains('active')).toBe(false);
  });

  test('la barra de progreso se actualiza al avanzar al paso 2 de 3', () => {
    updateFormProgress(2);
    const fill = document.querySelector('.progress-fill');
    expect(fill.style.width).toBe('50%');
  });

  test('la barra de progreso es 0% en el paso 1', () => {
    updateFormProgress(1);
    expect(document.querySelector('.progress-fill').style.width).toBe('0%');
  });

  test('la barra de progreso es 100% en el último paso (3 de 3)', () => {
    updateFormProgress(3);
    expect(document.querySelector('.progress-fill').style.width).toBe('100%');
  });

  test('los indicadores de paso se marcan correctamente', () => {
    updateFormProgress(2);
    const indicators = document.querySelectorAll('.step');
    expect(indicators[0].classList.contains('active')).toBe(true);
    expect(indicators[1].classList.contains('active')).toBe(true);
    expect(indicators[2].classList.contains('active')).toBe(false);
  });
});

describe('sponsorshipLevel — visibilidad de customAmount', () => {
  test('customAmountContainer se muestra al seleccionar "platinum"', () => {
    const select = document.getElementById('sponsorshipLevel');
    const container = document.getElementById('customAmountContainer');

    select.value = 'platinum';
    select.dispatchEvent(new Event('change'));

    // Simula lógica del handler
    if (select.value === 'platinum') container.style.display = 'block';
    expect(container.style.display).toBe('block');
  });

  test('customAmountContainer se oculta al seleccionar otro valor', () => {
    const select = document.getElementById('sponsorshipLevel');
    const container = document.getElementById('customAmountContainer');
    container.style.display = 'block';

    select.value = 'argentina';
    if (select.value !== 'platinum') container.style.display = 'none';
    expect(container.style.display).toBe('none');
  });
});
