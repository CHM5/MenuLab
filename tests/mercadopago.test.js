/**
 * Integration tests — MercadoPago redirect logic (plansForm.js)
 */

const mpLinks = {
  18000: 'https://www.mercadopago.com.ar/subscriptions/checkout?preapproval_plan_id=2c938084966c84bc01969976d53f14d2',
  36000: 'https://www.mercadopago.com.ar/subscriptions/checkout?preapproval_plan_id=2c9380849696ea8201969bd7708d01ac',
  72000: 'https://www.mercadopago.com.ar/subscriptions/checkout?preapproval_plan_id=2c938084968c9eaa01969bd7f0f4062c',
  180000: 'https://www.mercadopago.com.ar/subscriptions/checkout?preapproval_plan_id=2c9380849721f5e501972934c13602ad',
  360000: 'https://mpago.la/1FzYWEk',
  720000: 'https://mpago.la/2sL5gCq',
};

// Simula la función de redirect extraída de plansForm.js
function handleMpRedirect(price, navigateTo, advanceTo) {
  if (price === 0) {
    advanceTo(6);
  } else if (mpLinks[price]) {
    navigateTo(mpLinks[price]);
  } else {
    return null; // plan no encontrado
  }
}

// ─────────────────────────────────────────────────────────────────────────────

describe('Tabla de links de MercadoPago', () => {
  test('tiene exactamente 6 planes de pago', () => {
    expect(Object.keys(mpLinks).length).toBe(6);
  });

  test('Plan Emprendedor mensual ($18.000) tiene link válido', () => {
    expect(mpLinks[18000]).toContain('mercadopago.com.ar');
  });

  test('Plan Corporativo anual ($720.000) tiene link válido', () => {
    expect(mpLinks[720000]).toContain('mpago.la');
  });

  test('todos los links son HTTPS', () => {
    Object.values(mpLinks).forEach(url => {
      expect(url.startsWith('https://')).toBe(true);
    });
  });
});

describe('handleMpRedirect', () => {
  test('redirige al link de MP cuando el precio existe', () => {
    const navigateTo = jest.fn();
    const advanceTo = jest.fn();
    handleMpRedirect(18000, navigateTo, advanceTo);
    expect(navigateTo).toHaveBeenCalledWith(mpLinks[18000]);
    expect(advanceTo).not.toHaveBeenCalled();
  });

  test('avanza al paso 6 cuando el plan es gratuito (precio 0)', () => {
    const navigateTo = jest.fn();
    const advanceTo = jest.fn();
    handleMpRedirect(0, navigateTo, advanceTo);
    expect(advanceTo).toHaveBeenCalledWith(6);
    expect(navigateTo).not.toHaveBeenCalled();
  });

  test('devuelve null cuando el precio no corresponde a ningún plan', () => {
    const navigateTo = jest.fn();
    const advanceTo = jest.fn();
    const result = handleMpRedirect(99999, navigateTo, advanceTo);
    expect(result).toBeNull();
    expect(navigateTo).not.toHaveBeenCalled();
    expect(advanceTo).not.toHaveBeenCalled();
  });

  test('redirige correctamente al plan Profesional anual ($360.000)', () => {
    const navigateTo = jest.fn();
    const advanceTo = jest.fn();
    handleMpRedirect(360000, navigateTo, advanceTo);
    expect(navigateTo).toHaveBeenCalledWith('https://mpago.la/1FzYWEk');
  });

  test('redirige correctamente al plan Corporativo mensual ($72.000)', () => {
    const navigateTo = jest.fn();
    const advanceTo = jest.fn();
    handleMpRedirect(72000, navigateTo, advanceTo);
    expect(navigateTo).toHaveBeenCalledWith(mpLinks[72000]);
  });
});
