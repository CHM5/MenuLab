import os, re
import json
from pathlib import Path
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import hashlib

# === CONFIGURACIÓN ===
FIJOS_RANGE = "Datos!B2:B8"
MENU_RANGE = "Menu!A2:E"

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
restaurant_name = os.environ.get("NEGOCIO", "Restaurante").strip()
slug = re.sub(r'[^a-zA-Z0-9]+', '-', restaurant_name.lower()).strip('-')

output_dir = Path(f"menu/{slug}")
output_dir.mkdir(parents=True, exist_ok=True)
html_file = output_dir / "index.html"

print(f"🏷️ Restaurante: {restaurant_name}")
print(f"📂 Carpeta generada: {output_dir}")
print(f"🔗 URL pública: https://www.menulab.com.ar/menu/{slug}/")

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
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 10px; /* espacio entre firuletes y texto */
      font-size: calc(1.5 * var(--menu-font-size));
      color: var(--color-categoria);
      font-weight: bold;
      text-align: center;
      margin: 1.2rem 0 0.8rem;
    }}
    h2::before,
    h2::after {{
      content: var(--firulete, "✦ ✦ ✦");
      color: var(--color-categoria, #b28051);
      font-size: 1rem;
      opacity: 0.4;
      white-space: nowrap;
      flex-shrink: 0; /* evita que se encojan */
    }}

    h2::before {{
      left: calc(50% - 10rem); /* distancia desde el centro hacia la izquierda */
    }}

    h2::after {{
      right: calc(50% - 10rem); /* distancia desde el centro hacia la derecha */
    }}

    /* === DESTACADOS === */
    .category-highlight {{
      border: 2px solid var(--color-categoria);
      border-radius: 10px;
      padding: 8px 12px;
      margin: 1.5rem 0;
      background-color: rgba(255, 235, 200, 0.25);
      box-shadow: 0 0 6px rgba(0, 0, 0, 0.05);
      break-inside: avoid;
    }}

    .category-highlight h2 {{
      margin-top: 0.5rem;
    }}

    .category-highlight::before {{
      display: block;
      text-align: center;
      font-size: 0.8rem;
      color: var(--color-categoria, #b28051);
      font-style: italic;
      margin-bottom: 0.3rem;
      opacity: 0.8;
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
      padding: 0.4rem 0;
      break-inside: avoid-column;
      page-break-inside: avoid;
    }}

    /* === ICONOS DIETARIOS === */
    .icon-diet {{
      width: 18px;
      height: 18px;
      object-fit: contain;
      vertical-align: middle;
      margin-right: -10px;
      filter: drop-shadow(0 0 1px rgba(0,0,0,0.2));
    }}

    .diet-icons.inline {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      margin-right: 6px;
      margin-top: 0;
    }}

    .diet-icons.inline span {{
      line-height: 1;
      transform: translateY(2px);
    }}

    .menu-item.destacado {{
      background: color-mix(in srgb, var(--color-bg) 95%, black);
      border-radius: 6px;
      padding: 0.3rem 0.4rem;
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

  #colorMenu label{{
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:6px;
  }}

  #colorMenu .color-group{{
    width:18px;
    height:18px;
    accent-color:#457B9D;
  }}

  #colorMenu:not(.active) .color-group{{
    display:none;
  }}

  #colorMenu.active .color-group{{
    display:inline-block;
    cursor:pointer;
  }}

  #colorMenu.active label:hover{{
    background:#eef6fa;
    border-radius:4px;
  }}

  #masterColorContainer {{
    display: none;
    justify-content: space-between;
    align-items: center;
  }}

  #colorMenu.active #masterColorContainer {{
    display: flex;
  }}

  #masterColor {{
    width: 32px;
    height: 32px;
    border: none;
    cursor: pointer;
    border-radius: 4px;
    transition: transform 0.2s ease;
  }}

  #masterColor:hover {{
    transform: scale(1.05);
  }}

  #presetSelector {{
    width: 100%;
    border-radius: 6px;
    border: 1px solid #ccc;
    padding: 6px;
    font-size: 0.9rem;
    cursor: pointer;
  }}
  </style>
<link href="https://fonts.googleapis.com/css?family=Oswald:400,700|Roboto+Slab:400,700|Pacifico|Lato:400,700|Merriweather:400,700|Montserrat:400,700|Indie+Flower|Playfair+Display:400,700|Source+Code+Pro:400,700&display=swap" rel="stylesheet">  
<link href="https://fonts.googleapis.com/css?family=Oswald:400,700&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Unbounded:wght@400;700&family=Syne:wght@400;700&family=Sora:wght@400;700&family=Staatliches&family=Caveat&family=Yeseva+One&family=Righteous&family=Cormorant+Garamond:wght@400;700&display=swap" rel="stylesheet">
</head>
<body>
  <div class="print-background"></div>
    <div id="topMenu">
      <div class="dropdown">
        <button class="dropbtn">🌈 Estilos</button>
        <div class="dropdown-content">
          <label for="presetSelector">Seleccionar estilo</label>
          <select id="presetSelector" style="width:100%;">
            <option value="">Seleccioná un estilo...</option>
            <option value="1">☕ Vintage</option>
            <option value="2">🌿 Natural Pastel</option>
            <option value="3">🖤 Minimalista Oscuro</option>
            <option value="4">💎 Luxury Dorado</option>
            <option value="5">📜 Clásico Italiano</option>
            <option value="6">🩵 Celeste Moderno</option>
            <option value="7">🍂 Otoñal Suave</option>
            <option value="8">⚡ Tech Futurista</option>
            <option value="9">🎨 Pop Alegre</option>
            <option value="10">🤍 Blanco Neutro</option>
          </select>
        </div>
      </div>
      <div class="dropdown">
        <button class="dropbtn">🖋️ Fuente</button>
        <div class="dropdown-content">
          <label for="fontSelector">Seleccionar fuente</label>
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
        <div class="dropdown-content" id="colorMenu">
          <label>Nombre <input type="checkbox" class="color-group"> <input type="color" id="color-nombre-resto"></label>
          <label>Slogan <input type="checkbox" class="color-group"> <input type="color" id="color-nombre-slogan"></label>
          <label>Categoria <input type="checkbox" class="color-group"> <input type="color" id="color-categoria"></label>
          <label>Subcategoria <input type="checkbox" class="color-group"> <input type="color" id="color-subcategoria"></label>
          <label>Plato <input type="checkbox" class="color-group"> <input type="color" id="color-plato"></label>
          <label>Descripción <input type="checkbox" class="color-group"> <input type="color" id="color-descripcion"></label>
          <label>Precio <input type="checkbox" class="color-group"> <input type="color" id="color-precio"></label>
          <label>Info <input type="checkbox" class="color-group"> <input type="color" id="color-info-resto"></label>
          <label>Fondo <input type="checkbox" class="color-group"> <input type="color" id="color-bg"></label>

          <hr style="margin:8px 0;">
          <label style="display:flex;align-items:center;gap:6px;font-size:0.85rem;">
            <input type="checkbox" id="sameColorMode">
            Aplicar mismo color a los seleccionados
          </label>
          <!-- Cuadradito principal de color -->
          <div id="masterColorContainer" style="display:none;align-items:center;gap:6px;margin-top:6px;">
            <label style="font-size:0.85rem;">Color principal</label>
            <input type="color" id="masterColor" value="#000000" style="width:40px;height:40px;cursor:pointer;border:none;border-radius:4px;">
          </div>
          <small style="display:block;color:#555;font-size:0.75rem;margin-top:4px;">
            (Marcá varios campos y elegí un color para aplicarlo a todos)
          </small>
        </div>
      </div>
      <div class="dropdown">
        <button class="dropbtn">✨ Firulete</button>
        <div class="dropdown-content">
          <label for="firuleteSelector">Tipo de firulete</label>
          <select id="firuleteSelector" style="width:100%;">
            <option value="">Ninguno</option>
            <option value="✦ ✦ ✦">Brillos ✦ ✦ ✦</option>
            <option value="⚜ ⚜ ⚜">Clásico ⚜ ⚜ ⚜</option>
            <option value="❧ ❧ ❧">Floral ❧ ❧ ❧</option>
            <option value="☕ ♡ ☕">Café ☕ ♡ ☕</option>
            <option value="🍃 ✿ 🍃">Natural 🍃 ✿ 🍃</option>
            <option value="✤ ✤ ✤">Sello ✤ ✤ ✤</option>
            <option value="⋄ ⋄ ⋄">Rombo ⋄ ⋄ ⋄</option>
            <option value="✨ 💫 ✨">Mágico ✨ 💫 ✨</option>
          </select>
        </div>
      </div>
      <div>
        <label for="bg-opacity">Logo</label>
        <input type="range" id="bg-opacity" min="0" max="0.5" step="0.01" value="0.2" style="width:80px;">
      </div>
      <button id="printBtn" onclick="window.print()">🖨️ Vista Previa</button>
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
      const [cat, sub, name, desc, price, ...flags] = cols.map(c => c.trim());
      if (!cat || !name) return;
      if (!grouped[cat]) grouped[cat] = {{}};
      const s = sub || "-";
      if (!grouped[cat][s]) grouped[cat][s] = [];
      grouped[cat][s].push({{ name, desc, price, flags }});
    }});
  Object.entries(grouped).forEach(([cat, subs]) => {{
    const catWrapper = document.createElement("div");
    const catTitle = document.createElement("h2");
    catTitle.textContent = cat;
    catWrapper.appendChild(catTitle);
    Object.entries(subs).forEach(([sub, items]) => {{
      if (sub && sub !== "-") {{
        const subTitle = document.createElement("h3");
        subTitle.textContent = sub;
        catWrapper.appendChild(subTitle);
      }}
      items.forEach(item => {{
        const div = document.createElement("div");
        div.className = "menu-item";
        if (item.flags.includes("destacado")) div.classList.add("destacado");

        const icons = [];
        if (item.flags.includes("celiaco")) {{
          icons.push('<img class="icon-diet" src="https://res.cloudinary.com/drxznqm61/image/upload/v1760150815/download_4_yulmty.png" alt="Sin TACC" title="Sin TACC">');
        }}
        if (item.flags.includes("vegano")) {{
          icons.push('<img class="icon-diet" src="https://res.cloudinary.com/drxznqm61/image/upload/v1760150943/download_5_pupphw.png" alt="Apto Vegano" title="Apto Vegano">');
        }}
        const iconsHTML = icons.length ? `<div class="diet-icons">${{icons.join("")}}</div>` : "";

        div.innerHTML = `
          <div class="menu-plate">
            <h4>
              <span class="diet-icons inline">${{iconsHTML}}</span>
              ${{item.nombre}}
            </h4>
            <p class="menu-description">${{item.desc || ""}}</p>
          </div>
          <span class="menu-price">${{item.price}}</span>
        `;
        catWrapper.appendChild(div);
      }});
    }});
    container.appendChild(catWrapper);
  }});
}}

fetch(FIJOS_URL)
  .then(r => r.text())
  .then(data => {{
    const rows = data.split("\\n").map(r => r.split(",").map(c => c.replace(/"/g, "").trim()));

    // ⚙️ En tu CSV, la info útil está en columna B (índice 1)
    const get = row => (rows[row] && rows[row][1]) ? rows[row][1] : "";

    document.getElementById("nombre-resto").textContent = get(1);   
    document.getElementById("subtitulo-resto").textContent = get(2);
    document.getElementById("direccion-resto").textContent = get(3);
    document.getElementById("horario-resto").textContent = get(4);
    document.getElementById("telefono-resto").textContent = get(5);

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

    document.getElementById('fontSelector').addEventListener('change', function(e) {{
      const val = e.target.value;
      if (val === 'arial') {{
        document.body.style.fontFamily = 'Arial, sans-serif';
      }} else if (val === 'oswald') {{
        document.body.style.fontFamily = "'Oswald', Arial, sans-serif";
      }} else if (val === 'roboto-slab') {{
        document.body.style.fontFamily = "'Roboto Slab', serif";
      }} else if (val === 'pacifico') {{
        document.body.style.fontFamily = "'Pacifico', cursive";
      }} else if (val === 'lato') {{
        document.body.style.fontFamily = "'Lato', Arial, sans-serif";
      }} else if (val === 'merriweather') {{
        document.body.style.fontFamily = "'Merriweather', serif";
      }} else if (val === 'montserrat') {{
        document.body.style.fontFamily = "'Montserrat', Arial, sans-serif";
      }} else if (val === 'indie-flower') {{
        document.body.style.fontFamily = "'Indie Flower', cursive";
      }} else if (val === 'playfair') {{
        document.body.style.fontFamily = "'Playfair Display', serif";
      }} else if (val === 'source-code') {{
        document.body.style.fontFamily = "'Source Code Pro', monospace";
      }} else if (val === 'unbounded') {{
        document.body.style.fontFamily = "'Unbounded', sans-serif";
      }} else if (val === 'syne') {{
        document.body.style.fontFamily = "'Syne', sans-serif";
      }} else if (val === 'sora') {{
        document.body.style.fontFamily = "'Sora', sans-serif";
      }} else if (val === 'staatliches') {{
        document.body.style.fontFamily = "'Staatliches', sans-serif";
      }} else if (val === 'caveat') {{
        document.body.style.fontFamily = "'Caveat', cursive";
      }} else if (val === 'yeseva-one') {{
        document.body.style.fontFamily = "'Yeseva One', serif";
      }} else if (val === 'righteous') {{
        document.body.style.fontFamily = "'Righteous', cursive";
      }} else if (val === 'cormorant-garamond') {{
        document.body.style.fontFamily = "'Cormorant Garamond', serif";
      }}
      localStorage.setItem('font-family', val);
    }});

  document.querySelectorAll('#topMenu input[type="color"]').forEach(input => {{
    input.addEventListener('input', function() {{
      const varName = this.id;
      const color = this.value;
      document.documentElement.style.setProperty(`--${{varName}}`, color);
      localStorage.setItem(varName, color);
    }});
  }});

  document.querySelectorAll('#topMenu input[type="color"]').forEach(input => {{
    const saved = localStorage.getItem(input.id);
    if (saved) {{
      input.value = saved;
      document.documentElement.style.setProperty(`--${{input.id}}`, saved);
    }}
  }});

    const savedFont = localStorage.getItem('font-family');
    if (savedFont) {{
      document.getElementById('fontSelector').value = savedFont;
      // Aplica la fuente guardada
      if (savedFont === 'arial') {{
        document.body.style.fontFamily = 'Arial, sans-serif';
      }} else if (savedFont === 'oswald') {{
        document.body.style.fontFamily = "'Oswald', Arial, sans-serif";
      }} else if (savedFont === 'roboto-slab') {{
        document.body.style.fontFamily = "'Roboto Slab', serif";
      }} else if (savedFont === 'pacifico') {{
        document.body.style.fontFamily = "'Pacifico', cursive";
      }} else if (savedFont === 'lato') {{
        document.body.style.fontFamily = "'Lato', Arial, sans-serif";
      }} else if (savedFont === 'merriweather') {{
        document.body.style.fontFamily = "'Merriweather', serif";
      }} else if (savedFont === 'montserrat') {{
        document.body.style.fontFamily = "'Montserrat', Arial, sans-serif";
      }} else if (savedFont === 'indie-flower') {{
        document.body.style.fontFamily = "'Indie Flower', cursive";
      }} else if (savedFont === 'playfair') {{
        document.body.style.fontFamily = "'Playfair Display', serif";
      }} else if (savedFont === 'source-code') {{
        document.body.style.fontFamily = "'Source Code Pro', monospace";
      }}
    }}
  const fontSizeInput = document.getElementById('font-size-range');
  fontSizeInput.value = localStorage.getItem('menu-font-size') || '1';
  document.documentElement.style.setProperty('--menu-font-size', fontSizeInput.value + 'rem');
  fontSizeInput.addEventListener('input', function() {{
    document.documentElement.style.setProperty('--menu-font-size', this.value + 'rem');
    localStorage.setItem('menu-font-size', this.value);
  }});
    const savedFontSize = localStorage.getItem('menu-font-size');
    if (savedFontSize) {{
      fontSizeInput.value = savedFontSize;
      document.documentElement.style.setProperty('--menu-font-size', savedFontSize + 'rem');
    }}

    const bgOpacityInput = document.getElementById('bg-opacity');
    bgOpacityInput.value = localStorage.getItem('bg-opacity') || '0.2';
    document.documentElement.style.setProperty('--bg-opacity', bgOpacityInput.value);

    bgOpacityInput.addEventListener('input', function() {{
      document.documentElement.style.setProperty('--bg-opacity', this.value);
      localStorage.setItem('bg-opacity', this.value);
    }});
    const savedBgOpacity = localStorage.getItem('bg-opacity');
    if (savedBgOpacity) {{
      bgOpacityInput.value = savedBgOpacity;
      document.documentElement.style.setProperty('--bg-opacity', savedBgOpacity);
    }}

    const firuleteSelector = document.getElementById("firuleteSelector");
    firuleteSelector.addEventListener("change", function () {{
      const val = this.value;
      document.documentElement.style.setProperty("--firulete", `"${{val}}"`);
      localStorage.setItem("firulete", val);
    }});

    const savedFirulete = localStorage.getItem("firulete");
    if (savedFirulete) {{
      firuleteSelector.value = savedFirulete;
      document.documentElement.style.setProperty("--firulete", `"${{savedFirulete}}"`);
    }}

    const sameColorToggle = document.getElementById("sameColorMode");
    const colorMenu = document.getElementById("colorMenu");
    const colorGroups = document.querySelectorAll(".color-group");
    const colorPickers = document.querySelectorAll('#colorMenu input[type="color"]');

    sameColorToggle.addEventListener("change", () => {{
      const active = sameColorToggle.checked;

      if (active) {{
        colorMenu.classList.add("active");
      }} else {{
        colorMenu.classList.remove("active");
      }}

      colorGroups.forEach(cb => (cb.checked = false));
    }});

    colorPickers.forEach(picker => {{
      picker.addEventListener("input", () => {{
        const selectedCheckboxes = Array.from(colorGroups).filter(cb => cb.checked);
        const newColor = picker.value;
        const varName = picker.id;

        document.documentElement.style.setProperty(`--${{varName}}`, newColor);
        localStorage.setItem(varName, newColor);

        if (sameColorToggle.checked && selectedCheckboxes.length > 1) {{
          selectedCheckboxes.forEach(cb => {{
            const input = cb.nextElementSibling;
            input.value = newColor;
            const name = input.id;
            document.documentElement.style.setProperty(`--${{name}}`, newColor);
            localStorage.setItem(name, newColor);
          }});
        }}
      }});
    }});

    const masterColorContainer = document.getElementById("masterColorContainer");
    const masterColorInput = document.getElementById("masterColor");

    sameColorToggle.addEventListener("change", () => {{
      masterColorContainer.style.display = sameColorToggle.checked ? "flex" : "none";
    }});

    masterColorInput.addEventListener("input", () => {{
      if (!sameColorToggle.checked) return;

      const newColor = masterColorInput.value;
      const selectedCheckboxes = Array.from(document.querySelectorAll("#colorMenu .color-group")).filter(cb => cb.checked);

      selectedCheckboxes.forEach(cb => {{
        const input = cb.nextElementSibling;
        input.value = newColor;
        const varName = input.id;
        document.documentElement.style.setProperty(`--${{varName}}`, newColor);
        localStorage.setItem(varName, newColor);
      }});
    }});

    const presets = {{
      1: {{
        font: 'cormorant-garamond',
        size: '1.0',
        colors: {{
          'color-nombre-resto': '#4b2e05',
          'color-nombre-slogan': '#8b5e34',
          'color-categoria': '#4b2e05',
          'color-subcategoria': '#6e4429',
          'color-plato': '#2b1a10',
          'color-descripcion': '#7a6241',
          'color-precio': '#4b2e05',
          'color-info-resto': '#4b2e05',
          'color-bg': '#fff7ec',
          'color-firulete': '#b28554'
        }},
        firulete: '⚜ ⚜ ⚜',
        bgOpacity: '0.2'
      }},
      2: {{ 
        font: 'lato',
        size: '1',
        colors: {{
          'color-nombre-resto': '#466c3f',
          'color-nombre-slogan': '#6d9964',
          'color-categoria': '#466c3f',
          'color-subcategoria': '#688c55',
          'color-plato': '#3a5037',
          'color-descripcion': '#6f8d6a',
          'color-precio': '#55784b',
          'color-info-resto': '#466c3f',
          'color-bg': '#f5f9f5',
          'color-firulete': '#55784b'
        }},
        firulete: '🍃 ✿ 🍃',
        bgOpacity: '0.15'
      }},
      3: {{
        font: 'montserrat',
        size: '1',
        colors: {{
          'color-nombre-resto': '#ffffff',
          'color-nombre-slogan': '#cccccc',
          'color-categoria': '#ffffff',
          'color-subcategoria': '#cccccc',
          'color-plato': '#ffffff',
          'color-descripcion': '#aaaaaa',
          'color-precio': '#ff6464',
          'color-info-resto': '#dddddd',
          'color-bg': '#121212',
          'color-firulete': '#888888'
        }},
        firulete: '⋄ ⋄ ⋄',
        bgOpacity: '0.3'
      }},
      4: {{ 
        font: 'playfair',
        size: '1.1',
        colors: {{
          'color-nombre-resto': '#c9a44c',
          'color-nombre-slogan': '#b8974a',
          'color-categoria': '#b8974a',
          'color-subcategoria': '#d4b76d',
          'color-plato': '#222',
          'color-descripcion': '#666',
          'color-precio': '#b8974a',
          'color-info-resto': '#444',
          'color-bg': '#fdfaf3',
          'color-firulete': '#b8974a'
        }},
        firulete: '✤ ✤ ✤',
        bgOpacity: '0.18'
      }},
      5: {{ 
        font: 'merriweather',
        size: '1',
        colors: {{
          'color-nombre-resto': '#8c1d1d',
          'color-nombre-slogan': '#bf4040',
          'color-categoria': '#8c1d1d',
          'color-subcategoria': '#bf4040',
          'color-plato': '#2e2e2e',
          'color-descripcion': '#5a5a5a',
          'color-precio': '#8c1d1d',
          'color-info-resto': '#5a5a5a',
          'color-bg': '#fff9f9',
          'color-firulete': '#a64242'
        }},
        firulete: '❧ ❧ ❧',
        bgOpacity: '0.2'
      }},
      6: {{
        font: 'sora',
        size: '1',
        colors: {{
          'color-nombre-resto': '#004E89',
          'color-nombre-slogan': '#2F80ED',
          'color-categoria': '#004E89',
          'color-subcategoria': '#0077B6',
          'color-plato': '#333',
          'color-descripcion': '#555',
          'color-precio': '#0077B6',
          'color-info-resto': '#004E89',
          'color-bg': '#EAF6FF',
          'color-firulete': '#0077B6'
        }},
        firulete: '✦ ✦ ✦',
        bgOpacity: '0.12'
      }},
      7: {{
        font: 'yeseva-one',
        size: '1',
        colors: {{
          'color-nombre-resto': '#b05b2b',
          'color-nombre-slogan': '#d4844c',
          'color-categoria': '#b05b2b',
          'color-subcategoria': '#d4844c',
          'color-plato': '#3c2b1f',
          'color-descripcion': '#6b4b36',
          'color-precio': '#b05b2b',
          'color-info-resto': '#5a4333',
          'color-bg': '#fff8f2',
          'color-firulete': '#b05b2b'
        }},
        firulete: '✤ ✤ ✤',
        bgOpacity: '0.18'
      }},
      8: {{ 
        font: 'unbounded',
        size: '1',
        colors: {{
          'color-nombre-resto': '#00C6CF',
          'color-nombre-slogan': '#00F0FF',
          'color-categoria': '#00C6CF',
          'color-subcategoria': '#00E5FF',
          'color-plato': '#E0E0E0',
          'color-descripcion': '#B0B0B0',
          'color-precio': '#00E5FF',
          'color-info-resto': '#FFFFFF',
          'color-bg': '#0A0A0A',
          'color-firulete': '#00E5FF'
        }},
        firulete: '⚡ ⚡ ⚡',
        bgOpacity: '0.25'
      }},
      9: {{ 
        font: 'righteous',
        size: '1',
        colors: {{
          'color-nombre-resto': '#F94144',
          'color-nombre-slogan': '#F8961E',
          'color-categoria': '#F3722C',
          'color-subcategoria': '#F9C74F',
          'color-plato': '#277DA1',
          'color-descripcion': '#577590',
          'color-precio': '#F94144',
          'color-info-resto': '#F9844A',
          'color-bg': '#FFF8F0',
          'color-firulete': '#F3722C'
        }},
        firulete: '✨ 💫 ✨',
        bgOpacity: '0.15'
      }},
      10: {{ 
        font: 'lato',
        size: '1',
        colors: {{
          'color-nombre-resto': '#222',
          'color-nombre-slogan': '#555',
          'color-categoria': '#333',
          'color-subcategoria': '#555',
          'color-plato': '#222',
          'color-descripcion': '#777',
          'color-precio': '#000',
          'color-info-resto': '#333',
          'color-bg': '#ffffff',
          'color-firulete': '#aaa'
        }},
        firulete: '⋄ ⋄ ⋄',
        bgOpacity: '0.1'
      }}
    }};

    document.getElementById('presetSelector').addEventListener('change', function() {{
      const val = this.value;
      if (!val || !presets[val]) return;
      const preset = presets[val];

      document.getElementById('fontSelector').value = preset.font;
      document.body.style.fontFamily = `'${{preset.font}}', sans-serif`;
      localStorage.setItem('font-family', preset.font);

      document.documentElement.style.setProperty('--menu-font-size', preset.size + 'rem');
      localStorage.setItem('menu-font-size', preset.size);

      for (const [key, color] of Object.entries(preset.colors)) {{
        document.documentElement.style.setProperty(`--${{key}}`, color);
        localStorage.setItem(key, color);
        const input = document.getElementById(key);
        if (input) input.value = color;
      }}

      document.documentElement.style.setProperty('--firulete', `"${{preset.firulete}}"`);
      localStorage.setItem('firulete', preset.firulete);
      document.getElementById('firuleteSelector').value = preset.firulete;

      document.documentElement.style.setProperty('--bg-opacity', preset.bgOpacity);
      localStorage.setItem('bg-opacity', preset.bgOpacity);
      document.getElementById('bg-opacity').value = preset.bgOpacity;
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
    f.write(f"menu/{slug}/index.html")
with open("sheet_url.txt", "w") as f:
    f.write(sheet_url)
