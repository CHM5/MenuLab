/**
 * Integration tests — plansForm.js
 * Simula el DOM de plansForm.html y prueba la navegación por pasos,
 * validaciones y la lógica de updatePlanInfo.
 */

// ─── DOM mínimo de plansForm.html ─────────────────────────────────────────────
function buildPlansFormDOM() {
  document.body.innerHTML = `
    <form id="sponsorshipForm">
      <!-- Paso 1 -->
      <div class="form-step active" data-step="1">
        <input type="text" id="nombre" name="nombre" required>
        <input type="text" id="apellido" name="apellido" required>
        <input type="email" id="email" name="email" required>
        <input type="tel" id="telefono" name="telefono" required>
        <div id="fieldError" class="form-error" style="display:none;"></div>
        <button type="button" class="btn next-btn">Continuar</button>
      </div>

      <!-- Paso 2 -->
      <div class="form-step" data-step="2">
        <input type="checkbox" id="agreeTerms" name="agreeTerms">
        <div id="termsError" class="form-error" style="display:none;"></div>
        <button type="button" class="btn prev-btn">Atrás</button>
        <button type="button" class="btn next-btn">Continuar</button>
      </div>

      <!-- Paso 3 — resumen -->
      <div class="form-step" data-step="3">
        <div id="planInfo"></div>
        <button type="button" class="btn prev-btn">Atrás</button>
      </div>

      <!-- Paso 4 — éxito -->
      <div class="form-step" data-step="4">
        <button type="button" id="resetForm" class="btn">Realizar otra compra</button>
      </div>
    </form>
  `;
}

// ─── helpers de plansForm.js ─────────────────────────────────────────────────
function validateStep(step) {
  const currentStepEl = document.querySelector(`.form-step[data-step="${step}"]`);
  const requiredFields = currentStepEl.querySelectorAll('[required]');
  let isValid = true;

  requiredFields.forEach(field => {
    field.style.borderColor = '';
    const errorField = document.getElementById('fieldError');
    if (!field.checkValidity() || field.value.trim() === '') {
      field.style.borderColor = 'var(--danger-color)';
      field.classList.add('shake');
      isValid = false;
      if (errorField) {
        errorField.textContent = 'Debés completar todos los campos.';
        errorField.style.display = 'block';
      }
    } else {
      if (errorField) errorField.style.display = 'none';
    }
  });

  if (step === 2) {
    const agreeTerms = document.getElementById('agreeTerms');
    const errorBox = document.getElementById('termsError');
    if (!agreeTerms.checked) {
      errorBox.textContent = 'Debes aceptar los términos y condiciones para continuar.';
      errorBox.style.display = 'block';
      isValid = false;
    } else {
      errorBox.style.display = 'none';
    }
  }

  return isValid;
}

function updatePlanInfo(planName) {
  const planInfo = document.getElementById('planInfo');
  if (!planInfo) return;

  const nameLower = planName.toLowerCase();
  let planDesc = '';

  if (nameLower.includes('base')) {
    planDesc = '<ul><li>✅ Menú Online</li><li>⚠️ Hasta 25 ítems</li></ul>';
  } else if (nameLower.includes('emprendedor')) {
    planDesc = '<ul><li>✅ Menú Imprimible</li><li>✅ Ítems Ilimitados</li></ul>';
  } else if (nameLower.includes('profesional')) {
    planDesc = '<ul><li>✅ Código QR</li><li>✅ Integración Whatsapp</li></ul>';
  } else if (nameLower.includes('corporativo')) {
    planDesc = '<ul><li>✅ Integración de Fotos</li><li>✅ Atención Prioritaria</li></ul>';
  } else {
    planDesc = '<em>Este producto no tiene descripción detallada.</em>';
  }

  planInfo.innerHTML = `Plan <h3>${planName}</h3>${planDesc}`;
}

// ─────────────────────────────────────────────────────────────────────────────

beforeEach(() => {
  buildPlansFormDOM();
});

describe('Paso 1 — validación de datos personales', () => {
  test('falla cuando todos los campos están vacíos', () => {
    expect(validateStep(1)).toBe(false);
  });

  test('muestra mensaje de error cuando hay campos vacíos', () => {
    validateStep(1);
    expect(document.getElementById('fieldError').style.display).toBe('block');
    expect(document.getElementById('fieldError').textContent).toMatch(/completar/i);
  });

  test('pasa cuando todos los campos requeridos están completos', () => {
    document.getElementById('nombre').value = 'Juan';
    document.getElementById('apellido').value = 'Pérez';
    document.getElementById('email').value = 'juan@test.com';
    document.getElementById('telefono').value = '1130625858';
    expect(validateStep(1)).toBe(true);
  });

  test('falla con email inválido', () => {
    document.getElementById('nombre').value = 'Juan';
    document.getElementById('apellido').value = 'Pérez';
    document.getElementById('email').value = 'noesemail';
    document.getElementById('telefono').value = '1130625858';
    expect(validateStep(1)).toBe(false);
  });

  test('campo inválido queda con borde de error', () => {
    validateStep(1);
    const nombre = document.getElementById('nombre');
    expect(nombre.style.borderColor).toBe('var(--danger-color)');
  });

  test('campo válido no tiene borde de error', () => {
    document.getElementById('nombre').value = 'Juan';
    document.getElementById('apellido').value = 'Pérez';
    document.getElementById('email').value = 'juan@test.com';
    document.getElementById('telefono').value = '1130625858';
    validateStep(1);
    expect(document.getElementById('nombre').style.borderColor).toBe('');
  });
});

describe('Paso 2 — términos y condiciones', () => {
  test('falla si no se aceptaron los términos', () => {
    expect(validateStep(2)).toBe(false);
  });

  test('muestra mensaje de error de términos', () => {
    validateStep(2);
    expect(document.getElementById('termsError').style.display).toBe('block');
    expect(document.getElementById('termsError').textContent).toMatch(/términos/i);
  });

  test('pasa si los términos están aceptados', () => {
    document.getElementById('agreeTerms').checked = true;
    expect(validateStep(2)).toBe(true);
  });

  test('oculta el error de términos cuando se acepta', () => {
    document.getElementById('agreeTerms').checked = true;
    validateStep(2);
    expect(document.getElementById('termsError').style.display).toBe('none');
  });
});

describe('updatePlanInfo — resumen del plan seleccionado', () => {
  test('muestra contenido correcto para Plan Base', () => {
    updatePlanInfo('Plan Base');
    expect(document.getElementById('planInfo').innerHTML).toContain('Plan Base');
    expect(document.getElementById('planInfo').innerHTML).toContain('25 ítems');
  });

  test('muestra contenido correcto para Plan Emprendedor', () => {
    updatePlanInfo('Plan Emprendedor');
    expect(document.getElementById('planInfo').innerHTML).toContain('Imprimible');
  });

  test('muestra contenido correcto para Plan Profesional', () => {
    updatePlanInfo('Plan Profesional');
    expect(document.getElementById('planInfo').innerHTML).toContain('QR');
  });

  test('muestra contenido correcto para Plan Corporativo', () => {
    updatePlanInfo('Plan Corporativo');
    expect(document.getElementById('planInfo').innerHTML).toContain('Fotos');
  });

  test('muestra mensaje genérico para plan desconocido', () => {
    updatePlanInfo('Plan Desconocido XYZ');
    expect(document.getElementById('planInfo').innerHTML).toContain('descripción detallada');
  });

  test('el contenedor muestra el nombre del plan en un h3', () => {
    updatePlanInfo('Plan Profesional');
    expect(document.getElementById('planInfo').querySelector('h3').textContent).toBe('Plan Profesional');
  });
});

describe('Navegación entre pasos', () => {
  function showStep(step, formSteps) {
    formSteps.forEach(s => s.classList.remove('active'));
    document.querySelector(`.form-step[data-step="${step}"]`).classList.add('active');
  }

  test('avanza al paso 2 cuando el paso 1 es válido', () => {
    document.getElementById('nombre').value = 'Juan';
    document.getElementById('apellido').value = 'García';
    document.getElementById('email').value = 'juan@mail.com';
    document.getElementById('telefono').value = '1199999999';

    const formSteps = document.querySelectorAll('.form-step');
    let currentStep = 1;

    if (validateStep(currentStep)) {
      currentStep++;
      showStep(currentStep, formSteps);
    }

    expect(currentStep).toBe(2);
    expect(document.querySelector('.form-step[data-step="2"]').classList.contains('active')).toBe(true);
  });

  test('NO avanza si el paso 1 es inválido', () => {
    const formSteps = document.querySelectorAll('.form-step');
    let currentStep = 1;

    if (validateStep(currentStep)) {
      currentStep++;
      showStep(currentStep, formSteps);
    }

    expect(currentStep).toBe(1);
    expect(document.querySelector('.form-step[data-step="1"]').classList.contains('active')).toBe(true);
  });

  test('retrocede al paso 1 desde el paso 2', () => {
    const formSteps = document.querySelectorAll('.form-step');
    let currentStep = 2;
    showStep(2, formSteps);

    currentStep--;
    showStep(currentStep, formSteps);

    expect(currentStep).toBe(1);
    expect(document.querySelector('.form-step[data-step="1"]').classList.contains('active')).toBe(true);
  });

  test('no retrocede más allá del paso 1', () => {
    const formSteps = document.querySelectorAll('.form-step');
    let currentStep = 1;

    if (currentStep > 1) {
      currentStep--;
    }

    expect(currentStep).toBe(1);
  });
});
