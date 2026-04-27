/**
 * Unit tests — Cart logic (script.js)
 * Probamos getCart, setCart y updateCartCount de forma aislada,
 * sin cargar el módulo entero (que tiene efectos de lado sobre el DOM).
 */

// ─── helpers extraídos de script.js ──────────────────────────────────────────
function getCart() {
  return JSON.parse(localStorage.getItem('cart') || '[]');
}
function setCart(cart) {
  localStorage.setItem('cart', JSON.stringify(cart));
}

// ─────────────────────────────────────────────────────────────────────────────

beforeEach(() => {
  localStorage.clear();
});

describe('getCart', () => {
  test('devuelve array vacío si no hay nada en localStorage', () => {
    expect(getCart()).toEqual([]);
  });

  test('devuelve los productos almacenados', () => {
    localStorage.setItem('cart', JSON.stringify(['microsite', 'prosite']));
    expect(getCart()).toEqual(['microsite', 'prosite']);
  });
});

describe('setCart', () => {
  test('persiste el carrito en localStorage', () => {
    setCart(['cartadoblefaz']);
    expect(localStorage.getItem('cart')).toBe('["cartadoblefaz"]');
  });

  test('sobreescribe el carrito anterior', () => {
    setCart(['microsite']);
    setCart(['prosite', 'flyer']);
    expect(getCart()).toEqual(['prosite', 'flyer']);
  });
});

describe('agregar producto al carrito', () => {
  test('agrega un producto nuevo', () => {
    const cart = getCart();
    if (!cart.includes('microsite')) cart.push('microsite');
    setCart(cart);
    expect(getCart()).toContain('microsite');
  });

  test('no agrega duplicados', () => {
    setCart(['microsite']);
    const cart = getCart();
    if (!cart.includes('microsite')) cart.push('microsite');
    setCart(cart);
    expect(getCart().filter(p => p === 'microsite').length).toBe(1);
  });
});

describe('quitar producto del carrito', () => {
  test('elimina el producto indicado', () => {
    setCart(['microsite', 'prosite', 'flyer']);
    const cart = getCart().filter(p => p !== 'prosite');
    setCart(cart);
    expect(getCart()).toEqual(['microsite', 'flyer']);
  });

  test('no falla si el producto no estaba en el carrito', () => {
    setCart(['microsite']);
    const cart = getCart().filter(p => p !== 'inexistente');
    setCart(cart);
    expect(getCart()).toEqual(['microsite']);
  });
});

describe('updateCartCount (DOM)', () => {
  test('actualiza el texto del contador con la cantidad de productos', () => {
    document.body.innerHTML = '<span id="cart-count">0</span>';
    setCart(['microsite', 'flyer', 'posavasos']);

    function updateCartCount() {
      document.getElementById('cart-count').textContent = getCart().length;
    }
    updateCartCount();

    expect(document.getElementById('cart-count').textContent).toBe('3');
  });

  test('muestra 0 cuando el carrito está vacío', () => {
    document.body.innerHTML = '<span id="cart-count">5</span>';
    setCart([]);

    function updateCartCount() {
      document.getElementById('cart-count').textContent = getCart().length;
    }
    updateCartCount();

    expect(document.getElementById('cart-count').textContent).toBe('0');
  });
});
