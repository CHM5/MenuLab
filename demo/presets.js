/* === ARCHIVO: presets.js === */
/* Contiene todas las configuraciones visuales predefinidas de MenuLab */

/* === ARCHIVO: presets.js (Presets 1–10 actualizados) === */
const presets = {
  // 🥩 1. Cocina Tradicional
  1: {
    fonts: {
      "nombre-resto": "Tangerine",
      "nombre-slogan": "Tangerine",
      "categoria": "Tangerine",
      "subcategoria": "Tangerine",
      "plato": "Tangerine",
      "descripcion": "Tangerine",
      "precio": "Tangerine",
      "info-resto": "Tangerine"
    },
    sizes: { categoria: 2.3, subcategoria: 1.3, plato: 1.3, descripcion: 0.9, precio: 1.4, info: 1.0 },
    colors: {
      "--color-nombre-resto": "#3b2407",
      "--color-nombre-slogan": "#3b2407",
      "--color-categoria": "#5c3a18",
      "--color-subcategoria": "#5c3a18",
      "--color-precio": "#b77b46",
      "--color-info-resto": "#5c3a18",
      "--bg-opacity": "0.22"
    },
    columns: 2,
    frame: { style: "double", color: "#5a4739", width: 3 },
    firulete: "🔥 🍖 🔥"
  },

  // 🍷 2. Bodegón
  2: {
    fonts: {
      "nombre-resto": "Milonga",
      "nombre-slogan": "Playfair Display",
      "categoria": "Playfair Display",
      "subcategoria": "Merriweather",
      "plato": "Cormorant Garamond",
      "descripcion": "Merriweather",
      "precio": "Cinzel",
      "info-resto": "Milonga"
    },
    sizes: { categoria: 2.0, subcategoria: 1.2, plato: 1.3, descripcion: 0.95, precio: 1.3, info: 1.0 },
    colors: {
      "--color-nombre-resto": "#4a2c16",
      "--color-nombre-slogan": "#4a2c16",
      "--color-categoria": "#7b4b2a",
      "--color-subcategoria": "#7b4b2a",
      "--color-precio": "#a17c54",
      "--color-info-resto": "#7b4b2a",
      "--bg-opacity": "0.25"
    },
    columns: 2,
    frame: { style: "groove", color: "#8d6e63", width: 2 },
    firulete: "🍷 🕯️ 🍷"
  },

  // 🍽️ 3. Restaurante Clásico
  3: {
    fonts: {
      "nombre-resto": "Playfair Display",
      "nombre-slogan": "Merriweather",
      "categoria": "Merriweather",
      "subcategoria": "Playfair Display",
      "plato": "Montserrat",
      "descripcion": "Lato",
      "precio": "Playfair Display",
      "info-resto": "Playfair Display"
    },
    sizes: { categoria: 2.2, subcategoria: 1.3, plato: 1.3, descripcion: 1.0, precio: 1.3, info: 1.0 },
    colors: {
      "--color-nombre-resto": "#2e2e2e",
      "--color-nombre-slogan": "#2e2e2e",
      "--color-categoria": "#555",
      "--color-subcategoria": "#555",
      "--color-precio": "#b4976b",
      "--color-info-resto": "#555",
      "--bg-opacity": "0.18"
    },
    columns: 2,
    frame: { style: "solid", color: "#b4976b", width: 1 },
    firulete: "🥂 ✨ 🥂"
  },

  // 🥘 4. Comedor Familiar
  4: {
    fonts: {
      "nombre-resto": "Lato",
      "nombre-slogan": "Open Sans",
      "categoria": "Merriweather",
      "subcategoria": "Merriweather",
      "plato": "Nunito",
      "descripcion": "Open Sans",
      "precio": "Lato",
      "info-resto": "Lato"
    },
    sizes: { categoria: 2.0, subcategoria: 1.2, plato: 1.2, descripcion: 1.0, precio: 1.2, info: 0.9 },
    colors: {
      "--color-nombre-resto": "#333",
      "--color-nombre-slogan": "#333",
      "--color-categoria": "#555",
      "--color-subcategoria": "#555",
      "--color-precio": "#777",
      "--color-info-resto": "#555",
      "--bg-opacity": "0.12"
    },
    columns: 1,
    frame: { style: "none", color: "#ccc", width: 0 },
    firulete: "🍽️ 🕯️ 🍽️"
  },

  // 🍳 5. Rotisería
  5: {
    fonts: {
      "nombre-resto": "Oswald",
      "nombre-slogan": "Anton",
      "categoria": "Montserrat",
      "subcategoria": "Montserrat",
      "plato": "Anton",
      "descripcion": "Lato",
      "precio": "Oswald",
      "info-resto": "Oswald"
    },
    sizes: { categoria: 2.1, subcategoria: 1.2, plato: 1.3, descripcion: 1.0, precio: 1.4, info: 0.9 },
    colors: {
      "--color-nombre-resto": "#272727",
      "--color-nombre-slogan": "#272727",
      "--color-categoria": "#e67e22",
      "--color-subcategoria": "#e67e22",
      "--color-precio": "#333",
      "--color-info-resto": "#e67e22",
      "--bg-opacity": "0.15"
    },
    columns: 2,
    frame: { style: "solid", color: "#e67e22", width: 2 },
    firulete: "🥘 🔥 🥘"
  },

  // ☕ 6. Cafetería Elegante
  6: {
    fonts: {
      "nombre-resto": "Playfair Display",
      "nombre-slogan": "Cormorant Garamond",
      "categoria": "Cormorant Garamond",
      "subcategoria": "Merriweather",
      "plato": "Merriweather",
      "descripcion": "Quicksand",
      "precio": "Cormorant Garamond",
      "info-resto": "Playfair Display"
    },
    sizes: { categoria: 2.2, subcategoria: 1.3, plato: 1.3, descripcion: 0.9, precio: 1.1, info: 1.0 },
    colors: {
      "--color-nombre-resto": "#4e342e",
      "--color-nombre-slogan": "#4e342e",
      "--color-categoria": "#795548",
      "--color-subcategoria": "#795548",
      "--color-precio": "#3e2723",
      "--color-info-resto": "#795548",
      "--bg-opacity": "0.25"
    },
    columns: 2,
    frame: { style: "groove", color: "#8d6e63", width: 2 },
    firulete: "☕ 💝 ☕"
  },

  // 🥐 7. Panadería Artesanal
  7: {
    fonts: {
      "nombre-resto": "Amatic SC",
      "nombre-slogan": "Pacifico",
      "categoria": "Pacifico",
      "subcategoria": "Pacifico",
      "plato": "Cormorant Garamond",
      "descripcion": "Quicksand",
      "precio": "Oswald",
      "info-resto": "Amatic SC"
    },
    sizes: { categoria: 2.1, subcategoria: 1.3, plato: 1.3, descripcion: 1.0, precio: 1.3, info: 1.0 },
    colors: {
      "--color-nombre-resto": "#bf8040",
      "--color-nombre-slogan": "#bf8040",
      "--color-categoria": "#c97b2a",
      "--color-subcategoria": "#c97b2a",
      "--color-precio": "#8b4513",
      "--color-info-resto": "#c97b2a",
      "--bg-opacity": "0.22"
    },
    columns: 2,
    frame: { style: "dotted", color: "#c97b2a", width: 2 },
    firulete: "🥐 🌾 🥐"
  },

  // 🧁 8. Pastelería
  8: {
    fonts: {
      "nombre-resto": "Merriweather",
      "nombre-slogan": "Pacifico",
      "categoria": "Dancing Script",
      "subcategoria": "Sora",
      "plato": "Quicksand",
      "descripcion": "Sora",
      "precio": "Pacifico",
      "info-resto": "Merriweather"
    },
    sizes: { categoria: 2.0, subcategoria: 1.2, plato: 1.2, descripcion: 0.9, precio: 1.4, info: 1.0 },
    colors: {
      "--color-nombre-resto": "#ffb6c1",
      "--color-nombre-slogan": "#ffb6c1",
      "--color-categoria": "#e57373",
      "--color-subcategoria": "#e57373",
      "--color-precio": "#c2185b",
      "--color-info-resto": "#e57373",
      "--bg-opacity": "0.25"
    },
    columns: 2,
    frame: { style: "double", color: "#f48fb1", width: 2 },
    firulete: "🧁 🎀 🧁"
  },

  // 🍫 9. Chocolatería
  9: {
    fonts: {
      "nombre-resto": "Cormorant Garamond",
      "nombre-slogan": "Cormorant Garamond",
      "categoria": "Cinzel",
      "subcategoria": "Playfair Display",
      "plato": "Playfair Display",
      "descripcion": "Lato",
      "precio": "Cormorant Garamond",
      "info-resto": "Cormorant Garamond"
    },
    sizes: { categoria: 2.0, subcategoria: 1.3, plato: 1.3, descripcion: 1.0, precio: 1.4, info: 1.0 },
    colors: {
      "--color-nombre-resto": "#4b2e05",
      "--color-nombre-slogan": "#4b2e05",
      "--color-categoria": "#7b3f00",
      "--color-subcategoria": "#7b3f00",
      "--color-precio": "#2e1503",
      "--color-info-resto": "#7b3f00",
      "--bg-opacity": "0.22"
    },
    columns: 2,
    frame: { style: "solid", color: "#7b3f00", width: 3 },
    firulete: "🍫 💝 🍫"
  },

  // 🍵 10. Casa de Té
  10: {
    fonts: {
      "nombre-resto": "Tangerine",
      "nombre-slogan": "Tangerine",
      "categoria": "Playfair Display",
      "subcategoria": "Cormorant Garamond",
      "plato": "Cormorant Garamond",
      "descripcion": "Quicksand",
      "precio": "Sora",
      "info-resto": "Playfair Display"
    },
    sizes: { categoria: 2.2, subcategoria: 1.3, plato: 1.3, descripcion: 1.0, precio: 1.1, info: 1.0 },
    colors: {
      "--color-nombre-resto": "#3e6b48",
      "--color-nombre-slogan": "#3e6b48",
      "--color-categoria": "#81c784",
      "--color-subcategoria": "#81c784",
      "--color-precio": "#2e7d32",
      "--color-info-resto": "#81c784",
      "--bg-opacity": "0.18"
    },
    columns: 1,
    frame: { style: "dotted", color: "#a5d6a7", width: 2 },
    firulete: "🍵 🌿 🍵"
  },
  
  // 🍺 Bares y Nocturnos
  11: { fonts: { nombre: 'Oswald', categoria: 'Monoton' },
    colors: { '--color-nombre-resto': '#f1f1f1', '--color-categoria': '#ffb703', '--color-precio': '#ffb703', '--bg-opacity': '0.1' },
    columns: 3, frame: { style: 'none', color: '#222', width: 0 }, firulete: '🍺 🎵 🍺'
  },
  12: { fonts: { nombre: 'Sora', categoria: 'Montserrat' },
    colors: { '--color-nombre-resto': '#e639a6', '--color-categoria': '#ffd166', '--color-precio': '#06d6a0', '--bg-opacity': '0.2' },
    columns: 2, frame: { style: 'dashed', color: '#e639a6', width: 2 }, firulete: '🍸 🍋 🍸'
  },
  13: { fonts: { nombre: 'Ranchers', categoria: 'Oswald' },
    colors: { '--color-nombre-resto': '#fff', '--color-categoria': '#ff006e', '--color-precio': '#fb5607', '--bg-opacity': '0.15' },
    columns: 3, frame: { style: 'solid', color: '#222', width: 2 }, firulete: '🎵 💫 🎵'
  },
  14: { fonts: { nombre: 'Montserrat', categoria: 'Playfair Display' },
    colors: { '--color-nombre-resto': '#1d3557', '--color-categoria': '#457b9d', '--color-precio': '#a8dadc', '--bg-opacity': '0.15' },
    columns: 2, frame: { style: 'solid', color: '#457b9d', width: 1 }, firulete: '🥂 ✨ 🥂'
  },
  15: { fonts: { nombre: 'Monoton', categoria: 'Sora' },
    colors: { '--color-nombre-resto': '#fdfcdc', '--color-categoria': '#00bbf9', '--color-precio': '#ff006e', '--bg-opacity': '0.15' },
    columns: 3, frame: { style: 'solid', color: '#222', width: 1 }, firulete: '🌙 🎶 🌙'
  },
  // --- 🍔 Fast Food / Take Away ---
  16: { fonts: { nombre: 'Anton', categoria: 'Oswald' },
    colors: { '--color-nombre-resto': '#e63946', '--color-categoria': '#f77f00', '--color-precio': '#222', '--bg-opacity': '0.1' },
    columns: 3, frame: { style: 'solid', color: '#e63946', width: 2 }, firulete: '🍕 🔥 🍕'
  },
  17: { fonts: { nombre: 'Oswald', categoria: 'Anton' },
    colors: { '--color-nombre-resto': '#222', '--color-categoria': '#ffb703', '--color-precio': '#e63946', '--bg-opacity': '0.15' },
    columns: 3, frame: { style: 'dashed', color: '#ffb703', width: 2 }, firulete: '🍔 🍟 🍔'
  },
  18: { fonts: { nombre: 'Sora', categoria: 'Amatic SC' },
    colors: { '--color-nombre-resto': '#3a0ca3', '--color-categoria': '#f72585', '--color-precio': '#7209b7', '--bg-opacity': '0.1' },
    columns: 3, frame: { style: 'dotted', color: '#b5179e', width: 2 }, firulete: '🌮 🌶️ 🌮'
  },
  19: { fonts: { nombre: 'Amatic SC', categoria: 'Sora' },
    colors: { '--color-nombre-resto': '#e76f51', '--color-categoria': '#264653', '--color-precio': '#2a9d8f', '--bg-opacity': '0.1' },
    columns: 2, frame: { style: 'groove', color: '#264653', width: 2 }, firulete: '🥙 🔥 🥙'
  },
  20: { fonts: { nombre: 'Sora', categoria: 'Oswald' },
    colors: { '--color-nombre-resto': '#1b263b', '--color-categoria': '#e63946', '--color-precio': '#003049', '--bg-opacity': '0.15' },
    columns: 3, frame: { style: 'solid', color: '#eaeaea', width: 1 }, firulete: '🍣 🌸 🍣'
  },

  // --- 🥗 Saludables ---
  21: { fonts: { nombre: 'Quicksand', categoria: 'Sora' },
    colors: { '--color-nombre-resto': '#2e7d32', '--color-categoria': '#66bb6a', '--color-precio': '#1b5e20', '--bg-opacity': '0.15' },
    columns: 2, frame: { style: 'solid', color: '#66bb6a', width: 2 }, firulete: '🥑 🌿 🥑'
  },
  22: { fonts: { nombre: 'Nunito', categoria: 'Montserrat' },
    colors: { '--color-nombre-resto': '#388e3c', '--color-categoria': '#8bc34a', '--color-precio': '#4caf50', '--bg-opacity': '0.2' },
    columns: 2, frame: { style: 'dotted', color: '#8bc34a', width: 2 }, firulete: '🍏 🌱 🍏'
  },
  23: { fonts: { nombre: 'Lato', categoria: 'Sora' },
    colors: { '--color-nombre-resto': '#3f51b5', '--color-categoria': '#64b5f6', '--color-precio': '#1a237e', '--bg-opacity': '0.15' },
    columns: 2, frame: { style: 'solid', color: '#64b5f6', width: 2 }, firulete: '🍞 💙 🍞'
  },
  24: { fonts: { nombre: 'Playfair Display', categoria: 'Cormorant Garamond' },
    colors: { '--color-nombre-resto': '#2e7d32', '--color-categoria': '#81c784', '--color-precio': '#43a047', '--bg-opacity': '0.2' },
    columns: 1, frame: { style: 'none', color: '#ccc', width: 0 }, firulete: '🧘‍♂️ 🌿 🧘‍♂️'
  },
  25: { fonts: { nombre: 'Sora', categoria: 'Quicksand' },
    colors: { '--color-nombre-resto': '#558b2f', '--color-categoria': '#9ccc65', '--color-precio': '#7cb342', '--bg-opacity': '0.2' },
    columns: 2, frame: { style: 'solid', color: '#9ccc65', width: 2 }, firulete: '🌿 🌺 🌿'
  },

  // --- 🌍 Internacional ---
  26: { fonts: { nombre: 'Playfair Display', categoria: 'Cinzel' },
    colors: { '--color-nombre-resto': '#d4a373', '--color-categoria': '#99582a', '--color-precio': '#432818', '--bg-opacity': '0.15' },
    columns: 2, frame: { style: 'double', color: '#99582a', width: 2 }, firulete: '🍝 🇮🇹 🍝'
  },
  27: { fonts: { nombre: 'Sora', categoria: 'Noto Sans JP' },
    colors: { '--color-nombre-resto': '#1a1a1a', '--color-categoria': '#ff0000', '--color-precio': '#333', '--bg-opacity': '0.1' },
    columns: 3, frame: { style: 'solid', color: '#ff0000', width: 2 }, firulete: '🥟 🈵 🥟'
  },
  28: { fonts: { nombre: 'Amatic SC', categoria: 'Sora' },
    colors: { '--color-nombre-resto': '#e85d04', '--color-categoria': '#ffba08', '--color-precio': '#dc2f02', '--bg-opacity': '0.15' },
    columns: 3, frame: { style: 'solid', color: '#e85d04', width: 2 }, firulete: '🌮 🌶️ 🌮'
  },
  29: { fonts: { nombre: 'Cormorant Garamond', categoria: 'Playfair Display' },
    colors: { '--color-nombre-resto': '#b08968', '--color-categoria': '#7f5539', '--color-precio': '#9c6644', '--bg-opacity': '0.2' },
    columns: 2, frame: { style: 'groove', color: '#7f5539', width: 2 }, firulete: '🥘 🇪🇸 🥘'
  },
  30: { fonts: { nombre: 'Cinzel', categoria: 'Playfair Display' },
    colors: { '--color-nombre-resto': '#b5838d', '--color-categoria': '#ffb4a2', '--color-precio': '#6d6875', '--bg-opacity': '0.2' },
    columns: 2, frame: { style: 'solid', color: '#b5838d', width: 1 }, firulete: '🥖 🇫🇷 🥖'
  },

  // --- 🍦 Postres ---
  31: { fonts: { nombre: 'Pacifico', categoria: 'Quicksand' },
    colors: { '--color-nombre-resto': '#ffb6b9', '--color-categoria': '#fae3d9', '--color-precio': '#bbded6', '--bg-opacity': '0.25' },
    columns: 2, frame: { style: 'dotted', color: '#ffb6b9', width: 2 }, firulete: '🍰 🎀 🍰'
  },
  32: { fonts: { nombre: 'Montserrat', categoria: 'Amatic SC' },
    colors: { '--color-nombre-resto': '#4dd0e1', '--color-categoria': '#80deea', '--color-precio': '#0097a7', '--bg-opacity': '0.15' },
    columns: 2, frame: { style: 'solid', color: '#80deea', width: 2 }, firulete: '🍦 ❄️ 🍦'
  },
  33: { fonts: { nombre: 'Playfair Display', categoria: 'Cormorant Garamond' },
    colors: { '--color-nombre-resto': '#ff9e80', '--color-categoria': '#ffab91', '--color-precio': '#d84315', '--bg-opacity': '0.2' },
    columns: 2, frame: { style: 'double', color: '#ff9e80', width: 2 }, firulete: '🥧 🍓 🥧'
  },
  34: { fonts: { nombre: 'Amatic SC', categoria: 'Sora' },
    colors: { '--color-nombre-resto': '#ffb703', '--color-categoria': '#fb8500', '--color-precio': '#023047', '--bg-opacity': '0.15' },
    columns: 2, frame: { style: 'solid', color: '#fb8500', width: 2 }, firulete: '🧇 🍯 🧇'
  },
  35: { fonts: { nombre: 'Pacifico', categoria: 'Playfair Display' },
    colors: { '--color-nombre-resto': '#f48fb1', '--color-categoria': '#f06292', '--color-precio': '#880e4f', '--bg-opacity': '0.2' },
    columns: 2, frame: { style: 'dotted', color: '#f48fb1', width: 2 }, firulete: '🎂 💖 🎂'
  },

  // --- 🚚 Modernos ---
  36: { fonts: { nombre: 'Oswald', categoria: 'Sora' },
    colors: { '--color-nombre-resto': '#1a1a1a', '--color-categoria': '#fcbf49', '--color-precio': '#003049', '--bg-opacity': '0.1' },
    columns: 2, frame: { style: 'none', color: '#ccc', width: 0 }, firulete: '🚚 🍔 🚚'
  },
  37: { fonts: { nombre: 'Montserrat', categoria: 'Sora' },
    colors: { '--color-nombre-resto': '#264653', '--color-categoria': '#2a9d8f', '--color-precio': '#e9c46a', '--bg-opacity': '0.15' },
    columns: 2, frame: { style: 'solid', color: '#2a9d8f', width: 1 }, firulete: '🌆 ✨ 🌆'
  },
  38: { fonts: { nombre: 'Pacifico', categoria: 'Amatic SC' },
    colors: { '--color-nombre-resto': '#0077b6', '--color-categoria': '#00b4d8', '--color-precio': '#90e0ef', '--bg-opacity': '0.15' },
    columns: 1, frame: { style: 'solid', color: '#00b4d8', width: 2 }, firulete: '🏖️ 🌴 🏖️'
  },
  39: { fonts: { nombre: 'Sora', categoria: 'Montserrat' },
    colors: { '--color-nombre-resto': '#212121', '--color-categoria': '#607d8b', '--color-precio': '#455a64', '--bg-opacity': '0.1' },
    columns: 2, frame: { style: 'solid', color: '#607d8b', width: 1 }, firulete: '💡 🧠 💡'
  },
  40: { fonts: { nombre: 'Playfair Display', categoria: 'Cormorant Garamond' },
    colors: { '--color-nombre-resto': '#1d3557', '--color-categoria': '#457b9d', '--color-precio': '#a8dadc', '--bg-opacity': '0.15' },
    columns: 2, frame: { style: 'groove', color: '#457b9d', width: 2 }, firulete: '⚙️ ✨ ⚙️'
  }
};

/* === Aplicar preset === */
function applyPreset(id) {
  const preset = presets[id];
  if (!preset) return;

  // Esperar a que el iframe termine de renderizar el menú
  setTimeout(() => {
    // 🖋️ Fuentes
    Object.entries(preset.fonts || {}).forEach(([section, font]) => {
      sendToPreview("font-section", { section, font });
    });

    // 🔤 Tamaños
    Object.entries(preset.sizes || {}).forEach(([section, value]) => {
      sendToPreview("size-section", { section, value });
    });
  
    // 🎨 Colores
    Object.entries(preset.colors || {}).forEach(([section, value]) => {
      sendToPreview("color-section", { section, value });
    });

    // Columnas, marco, firulete
    sendToPreview("columns", preset.columns);
    sendToPreview("frame-style", preset.frame.style);
    sendToPreview("frame-color", preset.frame.color);
    sendToPreview("frame-width", preset.frame.width);
    sendToPreview("firulete", preset.firulete);
    sendToPreview("opacity", preset.colors["--bg-opacity"]);
  }, 300); // ⏱️ 300ms de espera
}

/* === Eventos === */
document.addEventListener("DOMContentLoaded", () => {
  setTimeout(() => {
    // volver a aplicar todos los colores, fuentes y tamaños almacenados en variables CSS
    const sections = [
      "nombre-resto",
      "nombre-slogan",
      "categoria",
      "subcategoria",
      "plato",
      "descripcion",
      "precio",
      "info-resto"
    ];

    sections.forEach(section => {
      const font = getComputedStyle(document.documentElement).getPropertyValue(`--font-${section}`)?.trim().replace(/['"]+/g, "");
      const color = getComputedStyle(document.documentElement).getPropertyValue(`--color-${section}`)?.trim();
      const size = getComputedStyle(document.documentElement).getPropertyValue(`--size-${section}`)?.trim();

      if (font)
        document.querySelectorAll(getSelector(section)).forEach(el => (el.style.fontFamily = `'${font}', sans-serif`));
      if (color)
        document.querySelectorAll(getSelector(section)).forEach(el => (el.style.color = color));
      if (size)
        document.querySelectorAll(getSelector(section)).forEach(el => (el.style.fontSize = size));
    });

    console.log("🔁 Refrescadas fuentes y colores en subcategorías y footer");
  }, 800); // ⏱️ espera 0.8s después del render
});

