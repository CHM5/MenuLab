/**
 * Unit tests — filterCategory (script.js)
 */

// ─── lógica extraída de script.js ────────────────────────────────────────────
let activeCategory = 'Sitio Web';

function filterCategory(category) {
  const cards = document.querySelectorAll('.product-card');
  const buttons = document.querySelectorAll('.toggle-button');

  if (activeCategory === category) {
    activeCategory = null;
    buttons.forEach(btn => btn.classList.remove('active'));
    cards.forEach(card => (card.style.display = 'block'));
    return;
  }

  activeCategory = category;
  buttons.forEach(btn => {
    btn.classList.toggle('active', btn.textContent === category);
  });

  cards.forEach(card => {
    const cat = card.querySelector('.product-category').textContent;
    card.style.display = cat === category ? 'block' : 'none';
  });
}
// ─────────────────────────────────────────────────────────────────────────────

function buildDOM() {
  document.body.innerHTML = `
    <button class="toggle-button">Sitio Web</button>
    <button class="toggle-button">Diseño de menú</button>
    <button class="toggle-button">Paquete</button>

    <div class="product-card"><div class="product-category">Sitio Web</div></div>
    <div class="product-card"><div class="product-category">Sitio Web</div></div>
    <div class="product-card"><div class="product-category">Diseño de menú</div></div>
    <div class="product-card"><div class="product-category">Paquete</div></div>
  `;
}

beforeEach(() => {
  buildDOM();
  activeCategory = null; // reset estado
});

describe('filterCategory', () => {
  test('filtra correctamente: solo muestra tarjetas de la categoría activa', () => {
    filterCategory('Diseño de menú');
    const cards = document.querySelectorAll('.product-card');
    expect(cards[0].style.display).toBe('none');   // Sitio Web
    expect(cards[1].style.display).toBe('none');   // Sitio Web
    expect(cards[2].style.display).toBe('block');  // Diseño de menú
    expect(cards[3].style.display).toBe('none');   // Paquete
  });

  test('activa la clase "active" solo en el botón correspondiente', () => {
    filterCategory('Sitio Web');
    const buttons = document.querySelectorAll('.toggle-button');
    expect(buttons[0].classList.contains('active')).toBe(true);
    expect(buttons[1].classList.contains('active')).toBe(false);
    expect(buttons[2].classList.contains('active')).toBe(false);
  });

  test('toggle: hacer clic dos veces en la misma categoría muestra todas las tarjetas', () => {
    filterCategory('Paquete');
    filterCategory('Paquete'); // segunda vez → deseleccionar

    const cards = document.querySelectorAll('.product-card');
    cards.forEach(card => {
      expect(card.style.display).toBe('block');
    });
  });

  test('toggle: hacer clic dos veces quita la clase active de todos los botones', () => {
    filterCategory('Sitio Web');
    filterCategory('Sitio Web');

    document.querySelectorAll('.toggle-button').forEach(btn => {
      expect(btn.classList.contains('active')).toBe(false);
    });
  });

  test('cambiar de categoría oculta las tarjetas anteriores y muestra las nuevas', () => {
    filterCategory('Sitio Web');
    filterCategory('Paquete');

    const cards = document.querySelectorAll('.product-card');
    expect(cards[0].style.display).toBe('none');  // Sitio Web
    expect(cards[1].style.display).toBe('none');  // Sitio Web
    expect(cards[3].style.display).toBe('block'); // Paquete
  });

  test('categoría inexistente oculta todas las tarjetas', () => {
    filterCategory('Inexistente');
    const cards = document.querySelectorAll('.product-card');
    cards.forEach(card => {
      expect(card.style.display).toBe('none');
    });
  });
});
