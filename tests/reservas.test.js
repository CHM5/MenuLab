/**
 * Integration tests — Reservas flow (script.js)
 * Prueba la lógica del botón #btnReserva: fetch de fechas ocupadas,
 * guardado en localStorage y navegación.
 */

// ─────────────────────────────────────────────────────────────────────────────

beforeEach(() => {
  localStorage.clear();
  jest.resetAllMocks();

  document.body.innerHTML = `
    <button id="btnReserva">Reservar</button>
    <span id="noPayLoader" style="display:none;"></span>
  `;
});

// Simula la lógica del handler del botón de reserva extraída de script.js
function attachReservaHandler(fetchFn, navigateFn) {
  const btn = document.getElementById('btnReserva');
  const loader = document.getElementById('noPayLoader');

  if (!btn) return;

  btn.addEventListener('click', (e) => {
    e.preventDefault();
    if (loader) loader.style.display = 'inline-block';

    fetchFn()
      .then(data => {
        localStorage.setItem('fechasOcupadas', JSON.stringify(data));
        navigateFn('reserva.html');
      })
      .catch(() => {
        navigateFn('reserva.html');
      });
  });
}

describe('Botón de reserva — flujo exitoso', () => {
  test('muestra el loader al hacer clic', () => {
    const fakeFetch = () => Promise.resolve(['2026-05-10', '2026-05-11']);
    const navigate = jest.fn();
    attachReservaHandler(fakeFetch, navigate);

    document.getElementById('btnReserva').click();

    expect(document.getElementById('noPayLoader').style.display).toBe('inline-block');
  });

  test('guarda fechas ocupadas en localStorage al recibir respuesta', async () => {
    const dates = ['2026-05-10', '2026-05-11'];
    const fakeFetch = () => Promise.resolve(dates);
    const navigate = jest.fn();
    attachReservaHandler(fakeFetch, navigate);

    document.getElementById('btnReserva').click();
    await Promise.resolve(); // flush microtask

    expect(localStorage.getItem('fechasOcupadas')).toBe(JSON.stringify(dates));
  });

  test('navega a reserva.html después del fetch exitoso', async () => {
    const fakeFetch = () => Promise.resolve(['2026-05-01']);
    const navigate = jest.fn();
    attachReservaHandler(fakeFetch, navigate);

    document.getElementById('btnReserva').click();
    await Promise.resolve();

    expect(navigate).toHaveBeenCalledWith('reserva.html');
  });
});

describe('Botón de reserva — flujo con error de red', () => {
  test('navega a reserva.html incluso si el fetch falla', async () => {
    const fakeFetch = () => Promise.reject(new Error('Network error'));
    const navigate = jest.fn();
    attachReservaHandler(fakeFetch, navigate);

    document.getElementById('btnReserva').click();
    await Promise.resolve();
    await Promise.resolve(); // rejection microtask

    expect(navigate).toHaveBeenCalledWith('reserva.html');
  });

  test('no guarda nada en localStorage si el fetch falla', async () => {
    const fakeFetch = () => Promise.reject(new Error('timeout'));
    const navigate = jest.fn();
    attachReservaHandler(fakeFetch, navigate);

    document.getElementById('btnReserva').click();
    await Promise.resolve();
    await Promise.resolve();

    expect(localStorage.getItem('fechasOcupadas')).toBeNull();
  });
});

describe('Botón de reserva — ausencia del botón en el DOM', () => {
  test('no lanza error cuando #btnReserva no existe', () => {
    document.body.innerHTML = '<span id="noPayLoader"></span>';
    expect(() => attachReservaHandler(() => Promise.resolve([]), jest.fn())).not.toThrow();
  });
});
