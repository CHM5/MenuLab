import os
import json
from pathlib import Path
from datetime import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import hashlib

# === CONFIGURACIÓN ===
FIJOS_RANGE = "Datos!B2:B8"
MENU_RANGE = "Menu!A2:E"
fecha_id = datetime.now().strftime("%Y%m%d")

# === AUTENTICACIÓN GOOGLE ===
credentials_info = json.loads(os.environ["GOOGLE_CREDENTIALS"])
creds = Credentials.from_service_account_info(
    credentials_info,
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
sheets_service = build("sheets", "v4", credentials=creds)

# === URL DE LA PLANILLA ===
sheet_url = os.environ["SHEET_URL"]
if not sheet_url:
    print("❌ SHEET_URL no provisto en las variables de entorno")
    exit(1)

# Extraer ID y armar URLs válidas
sheet_id = sheet_url.split("/d/")[1].split("/")[0]
csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Menu"
datos_csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Datos"
print("🔗 CSV menú:", csv_url)
print("🔗 CSV fijos:", datos_csv_url)

# === VALIDAR CONEXIÓN (sin cortar si falla) ===
try:
    sheets_service.spreadsheets().values().get(
        spreadsheetId=sheet_id, range=MENU_RANGE
    ).execute()
    print("✅ Conexión con Google Sheets verificada.")
except Exception as e:
    print(f"⚠️ Advertencia: no se pudo validar conexión con Sheets: {e}")

# === GENERAR HTML ===
# Generar hash único de 5 dígitos usando la fecha y la URL de la planilla
hash_input = f"{fecha_id}-{sheet_url}".encode("utf-8")
hash_str = hashlib.sha1(hash_input).hexdigest()[:5]

output_dir = Path(f"planes/menu-emprendedor-{fecha_id}-{hash_str}")
output_dir.mkdir(parents=True, exist_ok=True)
html_file = output_dir / "index.html"

html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <title>Menú Online</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
  <meta http-equiv="Pragma" content="no-cache">
  <meta http-equiv="Expires" content="0">
  <link rel="icon" type="image/png" href="../../MLfavicon.png" />
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css" integrity="sha512-SnH5WK+bZxgPHs44uWIX+LLJAJ9/2PkPKZ5QiAj6Ta86w+fsb2TkcmfRyVX3pBnMFcV7oQPJkl9QevSCWr3W6A==" crossorigin="anonymous" referrerpolicy="no-referrer" />
  <style>
    :root {{
      --nombre-restaurante: "Café Central";
      --subtitulo-restaurante: "Todo rico, todo el día";
      --direccion-restaurante: "Av. Corrientes 123";
      --horario-restaurante: "Martes a Domingos de 8 a 20hs";
      --telefono-restaurante: "+54 11 1234-5678";
      --color-nombre-resto: #000;
      --color-nombre-slogan: #000;
      --color-categoria: #000;
      --color-subcategoria: #000;
      --color-plato: #000;
      --color-descripcion: #555;
      --color-precio: #000;
      --color-info-resto: #000;
      --color-bg: #fff  ;
      --bg-opacity: 0.2;
      --menu-font-size: 1rem;
    }}

    @page {{
      @top-left {{ content: none; }}
      @top-center {{ content: none; }}
      @top-right {{ content: none; }}
      @bottom-left {{ content: none; }}
      @bottom-center {{ content: none; }}
      @bottom-right {{ content: none; }}
    }}
    
    body {{
      font-family: Arial, sans-serif;
      margin: 0 auto;
      padding-top: 70px; 
      column-count: 2;           
      column-gap: 20px;
      position: relative;
      background: var(--color-bg);
    }}

    #menuTable,
    .resto-header, .footer {{
      font-size: var(--menu-font-size);
    }}

    @media screen and (max-width: 991px) {{
      body {{
        margin-left: 10px;
        margin-right: 10px;
        column-count: 2;
        column-gap: 15px;
      }}
    }}

    @media screen and (min-width: 992px) {{
      body {{
        margin-left: 250px;
        margin-right: 250px;
        column-count: 2;
      }}
    }}


    h2 {{
      font-size: calc(1.5 * var(--menu-font-size)); 
      text-align: center; 
      break-after: avoid;
      page-break-after: avoid;
      text-decoration: underline;
      color: var(--color-categoria);
    }}
    h3 {{
      font-size: calc(1 * var(--menu-font-size)); 
      font-style: italic;
      text-align: left;
      break-after: avoid;
      page-break-after: avoid;
      color: var(--color-subcategoria);
    }}

    h4 {{
      font-size: calc(0.9 * var(--menu-font-size)); 
      margin: 0.2rem 0; 
    }}

    .menu-item {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      border-bottom: 1px solid #eee;
      padding: 0.4rem 0;
      break-inside: avoid-column;
      page-break-inside: avoid;
    }}

    .menu-plate {{
      flex: 1;
      color: var(--color-plato);
      display: flex;
      flex-direction: column;
    }}

    .menu-plate h4 {{
      margin: 0;
      font-size: calc(0.95 * var(--menu-font-size));
      font-weight: bold;
      color: var(--color-plato);
    }}

    .menu-description {{
      margin: 0.15rem 0 0;
      font-size: calc(0.8 * var(--menu-font-size));
      color: var(--color-descripcion);
    }}

    .menu-price {{
      font-weight: bold;
      font-size: calc(0.9 * var(--menu-font-size));
      color: var(--color-precio);
      margin-left: 12px;
      white-space: nowrap;
      align-self: flex-start;
    }}

    .dropbtn,
    #printBtn {{
      background-color: #67b0dd;
      color: white;
      padding: 10px 20px;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      font-size: 0.9rem;
      transition: background 0.3s ease;
    }}

    .dropbtn:hover,
    #printBtn:hover {{
      background-color: #1D3557;
    }}

    .footer {{
      column-span: all;
      text-align: center;
      font-size: calc(0.8 * var(--menu-font-size));
      color: #444;
      border-top: 1px solid #ddd;
      padding: 8px 0;
      background: var(--color-bg);
      position: relative;
      z-index: 10;
    }}

    .footer span {{
      margin: 0rem 8px;
      white-space: nowrap;
    }}

    #printArea {{
      column-count: 2;
      column-gap: 20px;
    }}

    @media print {{
    body {{
      margin-top: -70px !important;
      background: var(--color-bg) !important;
      column-count: 2 !important;
      column-gap: 15px !important;
      width: 210mm !important;
      max-width: 210mm !important;
      padding-bottom: 25mm !important;
    }}

    #printBtn, #topMenu {{
      display: none !important;
    }}

    #fontSelector,
    select#fontSelector,
    div > #fontSelector {{
      display: none !important;
    }}

    .footer {{
      position: fixed;
      bottom: 0mm;
      left: 0;
      right: 0;
      text-align: center;
      font-size: 0.7rem;
      border-top: 1px solid #ddd;
      background: var(--color-bg);
    }}

    @page {{
      size: A4;
      margin: 10mm 10mm 5mm 10mm;
    }}
        
    .print-background {{
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-size: 60%;
      opacity: var(--bg-opacity);
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }}
  }}

    .resto-header {{
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 1rem;
      margin-bottom: 1.5rem;
      break-inside: avoid;
    }}

    .resto-header img {{
      width: 100px;
      height: 100px;
      border-radius: 50%;
      object-fit: cover;
    }}

    .resto-text {{
      display: flex;
      flex-direction: column;
      align-items: flex-start;
    }}

    .resto-header h1 {{
      margin: 0;
      font-size: calc(2 * var(--menu-font-size));
    }}

    .resto-header h3 {{
      margin: 0.2rem 0 0;
      font-size: calc(1 * var(--menu-font-size));
      font-weight: normal;
      font-style: italic;
      color: #b28051;
    }}

    #nombre-resto {{
      color: var(--color-nombre-resto);
    }}

    #subtitulo-resto{{
      color: var(--color-nombre-slogan);
    }}

    #direccion-resto,
    #horario-resto,
    #telefono-resto {{
      color: var(--color-info-resto);
    }}

    #topMenu {{
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      background: #fff;
      padding: 10px 20px;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      z-index: 1000;
      display: flex;
      justify-content: center; 
      align-items: center;
      flex-wrap: wrap; 
      gap: 10px;
    }}

    .font-size-control,
    .opacity-control {{
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 4px;     
    }}

    #topMenu select {{
      padding: 6px 10px;
      border-radius: 6px;
      border: 1px solid #ddd;
      font-size: 0.9rem;
      cursor: pointer;
    }}

    #topMenu label {{
      font-size: 0.9rem;
      color: #333;
      display: flex;
      align-items: center;
      gap: 4px;
    }}

    #topMenu input[type="color"] {{
      width: 40px;
      height: 40px;
      border: none;
      padding: 0;
      cursor: pointer;
      border-radius: 4px;
      -webkit-appearance: none;
      appearance: none;
    }}

    #topMenu input[type="color"]::-webkit-color-swatch {{
      border: none;
      border-radius: 4px;
    }}

    #topMenu input[type="color"]::-webkit-color-swatch {{
      border: none;
      border-radius: 4px;
    }}

    #topMenu input[type="color"]:focus {{
      outline: none;
      box-shadow: 0 0 0 2px rgba(69, 123, 157, 0.5);
    }}

    .dropdown {{
      position: relative;
      display: inline-block;
    }}

    .dropbtn {{
      background-color: #67b0dd;
      color: white;
      padding: 10px 20px;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      font-size: 0.9rem;
    }}

    .dropdown-content {{
      display: none;
      position: absolute;
      background-color: #f9f9f9;
      min-width: 160px;
      box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
      z-index: 1;
      border-radius: 6px;
      padding: 10px;
    }}

    .dropdown-content label {{
      display: block;
      margin: 8px 0;
      font-size: 0.9rem;
      color: #333;
    }}

    .dropdown:hover .dropdown-content {{
      display: block;
    }}

    .print-background {{
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: url("https://res.cloudinary.com/drxznqm61/image/upload/v1759872998/drilldown-removebg-preview_zczol3.png")
                  no-repeat center center;
      background-size: 100%;
      opacity: var(--bg-opacity);
      z-index: 0;
      pointer-events: none;
    }}

    @media (max-width: 768px) {{
    #topMenu {{
      flex-direction: row;
      flex-wrap: wrap;
      justify-content: space-between;
      padding: 10px;
      gap: 6px;
    }}

    .font-size-control,
    .opacity-control {{
      width: 48%;
    }}

    .dropdown,
    #printBtn {{
      flex: 1 1 30%; 
      text-align: center;
    }}

    .dropbtn,
    #printBtn {{
      width: 100%;
      padding: 8px 0;
      font-size: 0.85rem;
    }}

    label {{
      font-size: 0.8rem;
    }}

    input[type="range"] {{
      width: 100%;
    }}
  }}

</style>
<link href="https://fonts.googleapis.com/css?family=Oswald:400,700|Roboto+Slab:400,700|Pacifico|Lato:400,700|Merriweather:400,700|Montserrat:400,700|Indie+Flower|Playfair+Display:400,700|Source+Code+Pro:400,700&display=swap" rel="stylesheet">  
<link href="https://fonts.googleapis.com/css?family=Oswald:400,700&display=swap" rel="stylesheet">
</head>
<body>
  <div class="print-background"></div>
  <div id="topMenu">
    <!-- panel controles como en código 1 -->
    <div class="dropdown">
      <button class="dropbtn">🖋️ Fuente</button>
      <div class="dropdown-content">
        <select id="fontSelector" style="width:100%;">
          <option value="arial">Arial (Actual)</option>
          <option value="oswald">Condensed Grotesk (Oswald)</option>
          <option value="roboto-slab">Serif Moderna (Roboto Slab)</option>
          <option value="pacifico">Manuscrita Cursiva (Pacifico)</option>
          <option value="lato">Sans Elegante (Lato)</option>
          <option value="merriweather">Serif Clásica (Merriweather)</option>
          <option value="montserrat">Sans Moderna (Montserrat)</option>
          <option value="indie-flower">Manuscrita Casual (Indie Flower)</option>
          <option value="playfair">Serif Fashion (Playfair Display)</option>
          <option value="source-code">Monoespaciada (Source Code Pro)</option>
          <option value="unbounded">Futurista Geométrica (Unbounded)</option>
          <option value="syne">Experimental Bold (Syne)</option>
          <option value="sora">Tech Elegante (Sora)</option>
          <option value="staatliches">Bauhaus Brutalista (Staatliches)</option>
          <option value="caveat">Manuscrita Clara (Caveat)</option>
          <option value="yeseva-one">Serif Chic (Yeseva One)</option>
          <option value="righteous">Redondeada Moderna (Righteous)</option>
          <option value="cormorant-garamond">Gourmet Serif (Cormorant Garamond)</option>
        </select>
      </div>
    </div>
    <div>
      <label for="font-size-range">Letra</label>
      <input type="range" id="font-size-range" min="0.7" max="2" step="0.01" value="1" style="width:80px;">
    </div>
    <div class="dropdown">
      <button class="dropbtn">🎨 Colores</button>
      <div class="dropdown-content">
        <label>Nombre <input type="color" id="color-nombre-resto"></label>
        <label>Slogan <input type="color" id="color-nombre-slogan"></label>
        <label>Categoria <input type="color" id="color-categoria"></label>
        <label>Subcategoria <input type="color" id="color-subcategoria"></label>
        <label>Plato <input type="color" id="color-plato"></label>
        <label>Descripción <input type="color" id="color-descripcion"></label>
        <label>Precio <input type="color" id="color-precio"></label>
        <label>Info <input type="color" id="color-info-resto"></label>
        <label>Fondo <input type="color" id="color-bg"></label>
      </div>
    </div>
    <div>
      <label for="bg-opacity">Logo</label>
      <input type="range" id="bg-opacity" min="0" max="0.5" step="0.01" value="0.2" style="width:80px;">
    </div>
    <button id="printBtn" onclick="window.print()">🖨️ Imprimir</button>
  </div>

  <div class="resto-header">
    <img id="perfil-resto" alt="Logo del restaurante" style="width:100px;height:100px;border-radius:50%;object-fit:cover;" hidden>
    <div class="resto-text">
      <h1 id="nombre-resto"></h1>
      <h3 id="subtitulo-resto"></h3>
    </div>
  </div>

  <div id="menuTable"></div>

  <div class="footer">
    <span><i class="fa-solid fa-map-marker-alt"></i> <span id="direccion-resto"></span></span> |
    <span><i class="fa-solid fa-clock"></i> <span id="horario-resto"></span></span> |
    <span><i class="fa-solid fa-phone"></i> <span id="telefono-resto"></span></span>
  </div>

<script>
  const CSV_URL = "{csv_url}";
  const FIJOS_URL = "{datos_csv_url}";
  let allRows = [];

  // === Cargar menú ===
  fetch(CSV_URL)
    .then(r => r.text())
    .then(data => {{
      allRows = data.split("\\n").slice(1).map(r => r.split(",").map(c => c.replace(/\"/g, "")));
      renderMenu(allRows);
    }});

  // === Renderizar menú agrupado ===
  function renderMenu(rows) {{
    const container = document.getElementById("menuTable");
    container.innerHTML = "";
    const grouped = {{}};
    rows.forEach(cols => {{
      const [cat, sub, name, desc, price] = cols.map(c => c.trim());
      if (!cat || !name) return;
      if (!grouped[cat]) grouped[cat] = {{}};
      const s = sub || "-";
      if (!grouped[cat][s]) grouped[cat][s] = [];
      grouped[cat][s].push({{ name, desc, price }});
    }});
    Object.entries(grouped).forEach(([cat, subs]) => {{
      const h2 = document.createElement("h2");
      h2.textContent = cat;
      container.appendChild(h2);
      Object.entries(subs).forEach(([sub, items]) => {{
        if (sub && sub !== "-") {{
          const h3 = document.createElement("h3");
          h3.textContent = sub;
          container.appendChild(h3);
        }}
        items.forEach(it => {{
          const div = document.createElement("div");
          div.className = "menu-item";
          div.innerHTML = `
            <div class="menu-plate">
              <h4>${{it.name}}</h4>
              <p class="menu-description">${{it.desc}}</p>
            </div>
            <span class="menu-price">${{it.price}}</span>`;
          container.appendChild(div);
        }});
      }});
    }});
  }}

fetch(FIJOS_URL)
  .then(r => r.text())
  .then(data => {{
    const rows = data.split("\n").map(r => r.split(",").map(c => c.replace(/"/g, "").trim()));

    // ⚙️ En tu CSV, la info útil está en columna B (índice 1)
    const get = row => (rows[row] && rows[row][1]) ? rows[row][1] : "";

    document.getElementById("nombre-resto").textContent = get(1);   // 🍸 Bar Menulab
    document.getElementById("subtitulo-resto").textContent = get(2); // ¡La mejor experiencia...
    document.getElementById("direccion-resto").textContent = get(3); // Av. Corrientes...
    document.getElementById("horario-resto").textContent = get(4);   // Horarios
    document.getElementById("telefono-resto").textContent = get(5);  // Teléfono

    const bg = get(6);   // Fondo
    const logo = get(7); // Logo

    if (bg && bg.toLowerCase() !== "off") {{
      const bgDiv = document.querySelector(".print-background");
      bgDiv.style.background = `url('${{bg}}') no-repeat center center`;
      bgDiv.style.backgroundSize = "100%";
    }}

    if (logo && logo.toLowerCase() !== "off") {{
      const img = document.getElementById("perfil-resto");
      img.src = logo;
      img.hidden = false;
    }}
  }});

  // Cambiar fuente
  document.getElementById('fontSelector').addEventListener('change', function(e) {{
    const val = e.target.value;
    const map = {{
      'arial': 'Arial, sans-serif',
      'oswald': "'Oswald', Arial, sans-serif",
      'roboto-slab': "'Roboto Slab', serif",
      'pacifico': "'Pacifico', cursive",
      'lato': "'Lato', Arial, sans-serif",
      'merriweather': "'Merriweather', serif",
      'montserrat': "'Montserrat', Arial, sans-serif",
      'indie-flower': "'Indie Flower', cursive",
      'playfair': "'Playfair Display', serif",
      'source-code': "'Source Code Pro', monospace",
      'unbounded': "'Unbounded', sans-serif",
      'syne': "'Syne', sans-serif",
      'sora': "'Sora', sans-serif",
      'staatliches': "'Staatliches', sans-serif",
      'caveat': "'Caveat', cursive",
      'yeseva-one': "'Yeseva One', serif",
      'righteous': "'Righteous', cursive",
      'cormorant-garamond': "'Cormorant Garamond', serif"
    }};
    document.body.style.fontFamily = map[val] || 'Arial, sans-serif';
    localStorage.setItem('font-family', val);
  }});

  // Restaurar fuente guardada
  const savedFont = localStorage.getItem('font-family');
  if (savedFont) {{
    document.getElementById('fontSelector').value = savedFont;
    document.body.style.fontFamily = map[savedFont] || 'Arial, sans-serif';
  }}

  // Cambiar colores
  document.querySelectorAll('#topMenu input[type="color"]').forEach(input => {{
    input.addEventListener('input', function() {{
      const varName = this.id;
      const color = this.value;
      document.documentElement.style.setProperty(`--${{varName}}`, color);
      localStorage.setItem(varName, color);
    }});
  }});

  // Restaurar colores
  document.querySelectorAll('#topMenu input[type="color"]').forEach(input => {{
    const saved = localStorage.getItem(input.id);
    if (saved) {{
      input.value = saved;
      document.documentElement.style.setProperty(`--${{input.id}}`, saved);
    }}
  }});

  // Cambiar tamaño de fuente
  const fontSizeInput = document.getElementById('font-size-range');
  fontSizeInput.value = localStorage.getItem('menu-font-size') || '1';
  document.documentElement.style.setProperty('--menu-font-size', fontSizeInput.value + 'rem');
  fontSizeInput.addEventListener('input', function() {{
    document.documentElement.style.setProperty('--menu-font-size', this.value + 'rem');
    localStorage.setItem('menu-font-size', this.value);
  }});

  // Restaurar opacidad fondo
  const bgOpacityInput = document.getElementById('bg-opacity');
  bgOpacityInput.value = localStorage.getItem('bg-opacity') || '0.2';
  document.documentElement.style.setProperty('--bg-opacity', bgOpacityInput.value);
  bgOpacityInput.addEventListener('input', function() {{
    document.documentElement.style.setProperty('--bg-opacity', this.value);
    localStorage.setItem('bg-opacity', this.value);
  }});


</script>
</body>
</html>
"""

# === GUARDAR HTML ===
with open(html_file, "w", encoding="utf-8") as f:
    f.write(html)

print("✅ HTML generado:", html_file)
print("📄 Planilla conectada:", sheet_url)

# === EXPORTAR PATHS PARA WORKFLOW ===
with open("menu_url.txt", "w") as f:
    f.write(f"planes/menu-emprendedor-{fecha_id}-{hash_str}/index.html")
with open("sheet_url.txt", "w") as f:
    f.write(sheet_url)
