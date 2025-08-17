import os
import json
from pathlib import Path
from datetime import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import hashlib

# === CONFIGURACIÓN ===
MENU_RANGE = "Menu!A2:F"
FIJOS_RANGE = "Datos Permanentes!B2:B17"
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
popup_csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Menu&range=B2"
menu_csv_url  = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Menu&range=A2:F"
fijos_csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Datos%20Permanentes"
personalizacion_csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Personalizacion"

print("🔗 CSV menú:", menu_csv_url )
print("🔗 CSV fijos:", fijos_csv_url)

# === VALIDAR CONEXIÓN (sin cortar si falla) ===
try:
    sheets_service.spreadsheets().values().get(
        spreadsheetId=sheet_id, range=MENU_RANGE
    ).execute()
    print("✅ Conexión con Google Sheets verificada.")
except Exception as e:
    print(f"⚠️ Advertencia: no se pudo validar conexión con Sheets: {e}")

# === OBTENER COLORES DE PERSONALIZACION ===
def rgb_to_hex(rgb):
    if not rgb:
        return "#ffffff"
    r = int(rgb.get("red", 1) * 255)
    g = int(rgb.get("green", 1) * 255)
    b = int(rgb.get("blue", 1) * 255)
    return f"#{r:02x}{g:02x}{b:02x}"


def pt_to_rem(pt: float) -> str:
    # 1pt ≈ 1.333px; 16px = 1rem
    px = float(pt) * 1.333
    return f"{px/16:.2f}rem"

def quote_family(fam: str) -> str:
    if not fam:
        return ""
    # Si tiene espacios o no es alfanumérico simple, comillas simples
    return f"'{fam}'" if any(ch.isspace() for ch in fam) else fam

def build_font_shorthand(tf: dict) -> str:
    """
    tf = textFormat dict de Sheets:
      { 'fontFamily': 'Segoe UI', 'fontSize': 12, 'bold': True, 'italic': True, ... }
    Devuelve ej: "italic bold 0.94rem 'Segoe UI', sans-serif"
    """
    if not tf:
        return ""

    parts = []
    if tf.get("italic"):
        parts.append("italic")
    if tf.get("bold"):
        parts.append("bold")

    size = tf.get("fontSize")
    if size:
        parts.append(pt_to_rem(size))

    fam = tf.get("fontFamily")
    if fam:
        parts.append(f"{quote_family(fam)}, sans-serif")

    return " ".join(parts).strip()

# Mapeo: variable CSS -> fila en Personalizacion (0-indexed)
css_map = [
    ("--businessName", 0),         # Encabezado
    ("--slogan", 1),         # Encabezado
    ("--address", 2),         # Encabezado
    ("--horarios", 3),         # Encabezado
    ("--textScrollbar", 4),  # Texto Categorías
    ("--title", 5),          # Categoría
    ("--subtitle", 6),       # Subcategoría
    ("--plate", 7),          # Plato
    ("--description", 8),    # Descripción
    ("--price", 9),          # Precio
    ("--bg", 10),             # Fondo
    ("--bgScrollbar", 11),    # Fondo Categorías
]
# Mapeo: nombre (col A en “Personalizacion”) -> variable CSS de fuente
FONT_VAR_MAP = {
    "Nombre del Negocio": "--font-businessName",
    "Eslogan": "--font-slogan",
    "Dirección": "--font-address",
    "Horarios": "--font-horarios",
    "Texto Categorías": "--font-textScrollbar",
    "Categoría": "--font-title",
    "Subcategoría": "--font-subtitle",
    "Plato": "--font-plate",
    "Descripción": "--font-description",
    "Precio": "--font-price",
}

def get_personalizacion_fonts(sheet_id: str) -> dict:
    """
    Lee Personalizacion!A2:B17 con includeGridData=True y arma { '--font-...': 'shorthand' }
    Si hay textFormatRuns, prioriza el primer run. Si no, usa effectiveFormat.textFormat.
    """
    fonts = {}
    try:
        resp = sheets_service.spreadsheets().get(
            spreadsheetId=sheet_id,
            ranges=["Personalizacion!A2:B17"],
            includeGridData=True,
            fields="sheets.data.rowData.values(effectiveFormat.textFormat,textFormatRuns,formattedValue)"
        ).execute()

        row_data = resp["sheets"][0]["data"][0].get("rowData", [])
        for row in row_data:
            cells = row.get("values", [])
            if len(cells) < 2:
                continue

            # Columna A: nombre (key)
            name = (cells[0].get("formattedValue") or "").strip()
            if not name:
                continue
            css_var = FONT_VAR_MAP.get(name)
            if not css_var:
                continue

            # Columna B: fuente
            cell_b = cells[1]
            # 1) Si hay textFormatRuns, usamos el primer run
            tf = None
            runs = cell_b.get("textFormatRuns")
            if runs and isinstance(runs, list) and runs:
                tf = runs[0].get("format", {})
            # 2) Sino, usamos effectiveFormat.textFormat
            if not tf:
                eff = cell_b.get("effectiveFormat", {})
                tf = eff.get("textFormat", {})

            shorthand = build_font_shorthand(tf)
            if shorthand:
                fonts[css_var] = shorthand

    except Exception as e:
        print("⚠️ No se pudieron obtener las fuentes de Personalizacion:", e)

    return fonts

personalizacion_colors = {}
personalizacion_fonts = get_personalizacion_fonts(sheet_id)

defaults_fonts = {
  "--font-businessName": "1.8rem 'Segoe UI', sans-serif",
  "--font-slogan": "italic 1rem 'Segoe UI', sans-serif",
  "--font-address": "italic 0.9rem 'Segoe UI', sans-serif",
  "--font-horarios": "italic 0.9rem 'Segoe UI', sans-serif",
  "--font-textScrollbar": "1rem 'Poppins', sans-serif",
  "--font-title": "1.7rem 'Poppins', sans-serif",
  "--font-subtitle": "1.5rem 'Poppins', Arial, sans-serif",
  "--font-plate": "1.2rem 'Poppins', sans-serif",
  "--font-description": "0.95rem 'Unbounded', cursive",
  "--font-price": "1.1rem 'Poppins', sans-serif",
}
for k, v in defaults_fonts.items():
    personalizacion_fonts.setdefault(k, v)


try:
    sheet = sheets_service.spreadsheets().get(
        spreadsheetId=sheet_id,
        ranges=["Personalizacion!C2:C17"],
        includeGridData=True,
        fields="sheets.data.rowData.values.effectiveFormat.backgroundColor"
    ).execute()
    rows = sheet["sheets"][0]["data"][0]["rowData"]
    for idx, (css_var, row_idx) in enumerate(css_map):
        color = rows[row_idx]["values"][0]["effectiveFormat"]["backgroundColor"]
        personalizacion_colors[css_var] = rgb_to_hex(color)
except Exception as e:
    print("⚠️ No se pudieron obtener los colores de Personalizacion:", e)
    # Defaults
    personalizacion_colors = {
        "--businessName": "#222222",
        "--slogan": "#444444",
        "--address": "#444444",
        "--horarios": "#444444",
        "--textScrollbar": "#fff",
        "--title": "#333",
        "--subtitle": "#555",
        "--plate": "#555",
        "--description": "#666",
        "--price": "#111",
        "--bg": "#f1f1f1",
        "--bgScrollbar": "#457B9D"
    }

# === GENERAR HTML ===
# Generar hash único de 5 dígitos usando la fecha y la URL de la planilla
hash_input = f"{fecha_id}-{sheet_url}".encode("utf-8")
hash_str = hashlib.sha1(hash_input).hexdigest()[:5]

output_dir = Path(f"planes/menu-corporativo-{fecha_id}-{hash_str}")
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
  <style>
    :root {{
      /* Colores */
      --businessName: {personalizacion_colors['--businessName']};
      --slogan: {personalizacion_colors['--slogan']};
      --address: {personalizacion_colors['--address']};
      --horarios: {personalizacion_colors['--horarios']};
      --textScrollbar: {personalizacion_colors['--textScrollbar']};
      --title: {personalizacion_colors['--title']};
      --subtitle: {personalizacion_colors['--subtitle']};
      --plate: {personalizacion_colors['--plate']};
      --description: {personalizacion_colors['--description']};
      --price: {personalizacion_colors['--price']};
      --bg: {personalizacion_colors['--bg']};
      --bgScrollbar: {personalizacion_colors['--bgScrollbar']};

      /* Fuentes */
      --font-businessName: {personalizacion_fonts['--font-businessName']};
      --font-slogan: {personalizacion_fonts['--font-slogan']};
      --font-address: {personalizacion_fonts['--font-address']};
      --font-horarios: {personalizacion_fonts['--font-horarios']};
      --font-textScrollbar: {personalizacion_fonts['--font-textScrollbar']};
      --font-title: {personalizacion_fonts['--font-title']};
      --font-subtitle: {personalizacion_fonts['--font-subtitle']};
      --font-plate: {personalizacion_fonts['--font-plate']};
      --font-description: {personalizacion_fonts['--font-description']};
      --font-price: {personalizacion_fonts['--font-price']};

      /* Bordes */
      --radius: 10px;
    }}
    body {{
      font-family: 'Segoe UI', Arial, sans-serif;
      background: var(--bg);
      margin: 0;
      padding: 0;
    }}
    header {{
      color: #fff;
      padding: 1.2rem 1rem 0.7rem 1rem;
      text-align: center;
      border-radius: 0 0 var(--radius) var(--radius);
    }}
    .container {{
      max-width: 900px;
      margin: 0 auto;
      padding: 1rem;
    }}
    .fijos {{
      margin: 1.5rem 0 1rem 0;
      padding: 0.7rem 1rem;
      background: #f8f9fa;
      border-radius: var(--radius);
      font-size: 1rem;
      color: #444;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 1rem;
      background: #fff;
      border-radius: var(--radius);
      overflow: hidden;
      box-shadow: 0 2px 8px #0001;
    }}
    th, td {{
      padding: 0.8rem 0.5rem;
      text-align: left;
      font-size: 1rem;
    }}
    th {{
      background: #f1f1f1;
      font-weight: 700;
      color: #343a40;
    }}
    tr:last-child td {{
      border-bottom: none;
    }}
    @media (max-width: 700px) {{
      .container {{
        padding: 0.5rem;
      }}
      th, td {{
        font-size: 0.97rem;
        padding: 0.6rem 0.3rem;
      }}
      .fijos {{
        font-size: 0.97rem;
        padding: 0.5rem 0.7rem;
      }}

    .menu-item-inner {{
      display: flex;
      align-items: center; /* Alinea verticalmente al centro */
    }}
    .menu-text {{
      width: 100%;
      text-align: left;
      flex: 1;
    }}
    .menu-img {{
      width: 100%;
      max-width: 180px;
      height: auto;
      margin-bottom: 0.5rem;
    }}
  }}

.menu-text {{
  flex: 1;
}}
    @media (max-width: 480px) {{
      header {{
        font-size: 1.2rem;
        padding: 0.8rem 0.3rem;
      }}
      .container {{
        padding: 0.2rem;
      }}
      th, td {{
        font-size: 0.93rem;
        padding: 0.4rem 0.2rem;
      }}
    }}
    .menu-group {{
      margin-top: 0.5rem;
      margin-bottom: 1.2rem;
    }}
    .menu-group h2 {{
      font: var(--font-title);
      color: var(--title); 
      margin: 2rem 0 0.2rem;
      border-bottom: 2px solid #ddd;
    }}
    .menu-group h3 {{
      font: var(--font-subtitle);
      color: var(--subtitle); 
      margin: 1rem 0 0rem;
    }}
    .menu-group h4 {{
      font: var(--font-plate);
      color: var(--plate);
      margin: 1rem 0 0rem;
    }}
    .menu-description {{
      font: var(--font-description);
      color: var(--description);
      margin: 0.2rem 0 0 0;
      padding: 0 1rem;
    }}
    .menu-price {{
      font: var(--font-price);
      color: var(--price);
      font-weight: 500;
    }}
    .menu-item {{
      border-bottom: 1px solid #eee;
      margin: -.5rem 0 -.5rem;
      padding: 0.8rem 0;
    }}
    .menu-item-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0 0.5rem;
    }}

    .menu-item-inner {{
      display: flex;
      align-items: flex-start;
      gap: 1rem;
      padding: 1rem;
      border-radius: 8px;
      background-color: #fff;
      box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    }}

    .menu-img {{
      width: 80px;
      height: 80px;
      object-fit: cover;
      border-radius: 10px;
      flex-shrink: 0;
    }}

    .menu-name {{
      font-size: 1.1rem;
      margin: 0;
      font-weight: 600;
    }}

  .menu-description {{
  margin: 0.2rem 0 0 0;
  font-size: 0.95rem;
  color: #666;
}}

.menu-price {{
  font-size: 1.1rem;
  font-weight: bold;
  color: #111;
  margin-top: 0.4rem;
}}

    @media (max-width: 600px) {{
      .menu-name {{
        font-size: 1rem;
      }}
      .menu-price {{
        font-size: 1rem;
      }}
      .menu-description {{
        font-size: 0.9rem;
      }}
    }}
    .menu-content {{
      margin-top: 2rem;
    }}
    .category-menu {{
      display: flex;
      gap: 12px;
      justify-content: center;
      align-items: center;
      margin: 0 0 0.5rem 0;
      flex-wrap: nowrap;
      overflow-x: auto;
      padding-top: 8px;
      padding-bottom: 8px;
      scrollbar-width: thin;
      scrollbar-color: var(--bgScrollbar) #eee;
      position: sticky;
      top: 50px;
      z-index: 1000;
    }}
    #categoryMenu {{
      margin-top: -0.2rem;
    }}
    .category-menu::-webkit-scrollbar {{
      height: 6px;
    }}
    .category-menu::-webkit-scrollbar-thumb {{
      background: var(--bgScrollbar); /* #457B9D */
      border-radius: 10px;
    }}
    .search-menu {{
      text-align: center;
      margin: 1rem 0;
      position: sticky;
      top: 0;
      padding-top: 8px;
    }}
    .category-btn {{
      font: var(--font-textScrollbar);
      background: var(--bgScrollbar);
      color: var(--textScrollbar);
      border: none;
      border-radius: 20px;
      padding: 7px 18px;
      font-weight: 600;
      cursor: pointer;
      transition: background 0.2s;
      flex: 0 0 auto;
    }}
    .category-btn:hover, .category-btn.active {{
      background: #457B9D;
    }}
    .header-flex {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      flex-wrap: wrap;
      gap: 0.5rem;
      font-family: 'Poppins', sans-serif;
    }}
    .header-left {{
      text-align: left;
      min-width: 200px;
      flex: 1 1 60px;
    }}
    .header-right {{
      text-align: right;
      min-width: 180px;
      flex: 1 1 180px;
    }}
    @media (max-width: 600px) {{
      .header-flex {{ flex-direction: column; gap: 0.2rem; margin-bottom: -100px; }}
      .header-left {{
        text-align: left;
        margin-top: 0px;
        margin-bottom: 0px;
        width: 100%;
      }}
      .header-right {{
        margin-top: 0.3rem;
        margin-bottom: 0px;
        width: 100%;
        min-width: unset;
      }}
      .header-left h1, .header-left h2 {{
        margin: 0.2rem 0; 
      }}
      .header-right div {{
        margin-top: 0.3rem; /* acercálo al bloque superior */
      }}
    }}
    /* Estilos para el botón de WhatsApp flotante */
    #whatsapp-float {{
      position: fixed;
      bottom: 20px;
      right: 20px;
      background: #25D366;
      color: white;
      border: none;
      border-radius: 50%;
      width: 56px;
      height: 56px;
      display: flex;
      justify-content: center;
      align-items: center;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
      z-index: 1000;
      transition: background 0.3s;
    }}

    #whatsapp-float:hover {{
      background: #128C7E;
    }}

    #whatsapp-float img {{
      width: 24px;
      height: 24px;
    }}

    .header-socials {{
        text-align: center;
        margin: 0rem 10px 0.5rem 10px;
        background-color: var(--bg); /* gris clarito */
        border-radius: 10px; /* bordes redondeados */
        padding: 0.5rem 1rem; /* opcional, para que respire */
    }}

    .header-socials a {{
      margin: 0 10px;
      display: inline-block;
    }}

    .header-socials img {{
      width: 30px;
      height: 30px;
      transition: transform 0.3s;
    }}

    .header-socials img:hover {{
      transform: scale(1.1);
    }}

    .pedido-checkbox {{
      accent-color: #E639A6;
      width: 12px;
      height: 12px;
    }}
    .menu-item.selected {{
      background: #457B9D !important; /* azul oscuro */
      color: #fff !important;
      border-radius: 10px;
      padding: 0rem 0rem;
    }}
    .menu-item.selected .menu-name,
    .menu-item.selected .menu-description,
    .menu-item.selected .menu-price {{
      color: #fff !important;
    }}
    .menu-item.selected .menu-img {{
      filter: none !important;
      opacity: 1 !important;
    }}
    .menu-item.selected .menu-item-inner {{
      background: transparent !important;
    }}

    .whatsapp-tooltip {{
      display: none;
      position: absolute;
      bottom: 70px;
      right: 0;
      background: rgba(0, 0, 0, 0.7);
      color: #fff;
      padding: 0.5rem;
      border-radius: 8px;
      font-size: 0.9rem;
      white-space: nowrap;
      z-index: 1001;
    }}

    #whatsapp-float:hover .whatsapp-tooltip {{
      display: block;
    }}

    .style-nombre {{
      font: var(--font-businessName);
      color:var(--businessName); 
      margin-bottom:0; 
      margin-top:0;
    }}
    .style-subtitulo {{
      font: var(--font-slogan);
      color:var(--slogan);
      margin:0.2rem 0 0.3rem 0;
      font-weight:400;
      font-style:italic;
    }}
    .style-direccion {{
      font: var(--font-address);
      color: var(--address);
    }}
    .style-horarios {{
      font: var(--font-horarios);
      color: var(--horarios);
    }}

  </style>
</head>
<body>
    <img id="banner-resto" src="" alt="Banner" style="width:100%;display:block;margin-bottom:0.5rem;">    
    <div class="container">
    <div class="header-flex">
      <div class="header-left">
        <h1 id="nombre-resto" class="style-nombre"></h1>
        <h2 id="subtitulo-resto" class="style-subtitulo"></h2>
      </div>
      <div class="header-right">
        <div><span id="direccion-resto" class="style-direccion"></span></div>
        <div><span id="horarios-resto" class="style-horarios"></span></div>
      </div>
    </div>
  </div>
  <div class="header-socials" id="headerSocials"></div>
  <div class="search-menu">
    <input
      id="menuSearch"
      type="text"
      placeholder="Buscar en la carta..."
      style="padding: 0.5rem 1rem; border-radius: 20px; border: 1px solid #ccc; width: 90%; max-width: 400px; font-size: 1rem;"
    />
  </div>
  <div id="categoryMenu" class="category-menu"></div>

  <div class="container">
    <div style="overflow-x:auto;">
      <div id="menuTable" class="menu-content"></div>
    </div>
    <div id="noResults" style="display:none;text-align:center;color:#dc3545;margin-top:1.5rem;font-size:1.1rem;">
      No se encontraron platos con ese criterio.
    </div>
  </div>

  <footer style="background:#f1f1f1;color:#333;text-align:center;padding:1rem 0 1.2rem 0;font-size:1rem;">
    <span class="thq-body-small">Desarrollado por</span>  
    <a href="https://menulab.com.ar" target="_blank" rel="noopener">
      <span style="display: inline-block; margin-left: 12px;">
        <h1 style="font-family: 'Unbounded', sans-serif; font-weight: 600; font-size: 100%; margin-left: -10px;
          background: linear-gradient(90deg, #E639A6, #457B9D);
          -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
          MenuLab
        </h1>
      </span>
    </a>
  </footer>
  <!-- Botón de WhatsApp flotante (sin href fijo) -->
  <a href="#" target="_blank" id="whatsapp-float" aria-label="WhatsApp">
    <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" alt="WhatsApp" style="width:56px;height:56px;">
  </a>
    
  <!-- Promo PopUp -->
  <div id="promoPopup" style="display:none; position:fixed; top:0; left:0; width:100vw; height:100vh; background:rgba(0,0,0,0.45); z-index:3000; justify-content:center; align-items:center;">
    <div id="promoContent" style="position:relative; background:#fff; border-radius:16px; box-shadow:0 4px 32px #0003; padding:0; max-width:90vw; max-height:80vh; display:flex; flex-direction:column; align-items:center;">
      <!-- Botón de cierre -->
      <button onclick="document.getElementById('promoPopup').style.display='none'" 
              style="position:absolute; top:10px; right:12px; background:transparent; border:none; font-size:1.5rem; color:#999; cursor:pointer;">
        &times;
      </button>
      <img id="promoImage" src="" alt="Promo de Temporada" 
          style="width:100%; max-width:400px; height:auto; border-radius:12px; display:block;">
      <!-- Puedes agregar texto o botón si querés -->
    </div>
  </div>
  <script data-cfasync="false">
    const POPUP_CSV_URL = "{popup_csv_url}";
    const CSV_URL = "{menu_csv_url }";
    const FIJOS_URL = "{fijos_csv_url}";
    const PERSONALIZACION_URL = "{personalizacion_csv_url}";

    let allRows = [];
    function renderCategoryMenu(rows) {{
      const categories = [...new Set(rows.map(r => r[0].trim()).filter(Boolean))];
      const menuDiv = document.getElementById('categoryMenu');
      menuDiv.innerHTML = '';

      categories.forEach(cat => {{
        const btn = document.createElement('button');
        btn.className = 'category-btn';
        btn.textContent = cat;
        btn.onclick = () => {{
          const section = document.querySelector(`.menu-group[data-cat="${{cat}}"]`);
          if (section) {{
            section.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
            document.querySelectorAll('.category-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
          }}
        }};
        menuDiv.scrollLeft = 0;
        menuDiv.appendChild(btn);
      }});
    }}

    function renderMenuGrouped(rows) {{
      const container = document.querySelector("#menuTable");
      container.innerHTML = "";

      const agrupado = {{}};

      rows.forEach(cols => {{
        const [cat, subcat, nombre, desc, precio, imagen] = cols.map(c => c.trim());
        if (!cat || !nombre) return;

        if (!agrupado[cat]) agrupado[cat] = {{}};
        const sub = subcat || "-";
        if (!agrupado[cat][sub]) agrupado[cat][sub] = [];
        agrupado[cat][sub].push({{ nombre, desc, precio, imagen }});
      }});

      Object.entries(agrupado).forEach(([cat, subcategorias]) => {{
        const group = document.createElement("div");
        group.className = "menu-group";
        group.setAttribute('data-cat', cat);

        const catTitle = document.createElement("h2");
        catTitle.textContent = cat;
        group.appendChild(catTitle);

        Object.entries(subcategorias).forEach(([subcat, items]) => {{
          if (subcat && subcat !== "-") {{
            const subTitle = document.createElement("h3");
            subTitle.textContent = subcat;
            group.appendChild(subTitle);
          }}

          items.forEach(item => {{
            const itemDiv = document.createElement("div");
            itemDiv.className = "menu-item";
            itemDiv.setAttribute("data-nombre", item.nombre);

            itemDiv.innerHTML = `
              <div class="menu-item-inner">
                <div class="menu-text">
                  <h4 class="menu-name">${{item.nombre}}</h4>
                  <p class="menu-description">${{item.desc}}</p>
                  <span class="menu-price">$${{item.precio}}</span>
                </div>
                ${{item.imagen ? `<img src="${{item.imagen}}" alt="${{item.nombre}}" class="menu-img">` : ""}}
              </div>
            `;

            // Selección visual y lógica
            itemDiv.addEventListener('click', function() {{
              itemDiv.classList.toggle('selected');
            }});

            group.appendChild(itemDiv);
          }});
        }});

        container.appendChild(group);
      }});
    }}

    function filterMenuRows(rows, query) {{
      if (!query) return rows;
      const q = query.trim().toLowerCase();
      return rows.filter(cols =>
        cols.some(cell => cell && cell.toLowerCase().includes(q))
      );
    }}

    const searchInput = document.getElementById('menuSearch');
    searchInput.addEventListener('input', function () {{
      const filtered = filterMenuRows(allRows, this.value);
      renderMenuGrouped(filtered);
      renderCategoryMenu(filtered);
      document.getElementById('noResults').style.display = filtered.length === 0 ? "block" : "none";
    }});

// === CSV robusto (soporta comillas) ===
function parseCSV(text) {{
  const rows = [];
  let row = [], cell = '', inQuotes = false;

  for (let i = 0; i < text.length; i++) {{
    const char = text[i], next = text[i + 1];

    if (char === '"') {{
      if (inQuotes && next === '"') {{ // comilla escapada
        cell += '"';
        i++;
      }} else {{
        inQuotes = !inQuotes;
      }}
    }} else if (char === ',' && !inQuotes) {{
      row.push(cell);
      cell = '';
    }} else if ((char === "\\n" || char === "\\r") && !inQuotes) {{
      if (cell.length || row.length) {{
        row.push(cell);
        rows.push(row);
        row = [];
        cell = '';
      }}
    }} else {{
      cell += char;
    }}
  }}
  if (cell.length || row.length) {{
    row.push(cell);
    rows.push(row);
  }}
  return rows;
}}

// --- POPUP: B2 directo (sin indexar filas) ---
fetch(POPUP_CSV_URL)
  .then(r => r.text())
  .then(txt => {{
    const url = txt.trim().replace(/^"|"$/g, ''); // quita comillas del CSV
    if (url && /^https?:\/\//i.test(url) && url.toLowerCase() !== 'off') {{
      const img = document.getElementById('promoImage');
      const pop = document.getElementById('promoPopup');
      if (img && pop) {{ img.src = url; pop.style.display = 'flex'; }}
    }}
  }})
  .catch(console.error);

// MENÚ: A2:F directo
fetch(CSV_URL)
  .then(r => r.text())
  .then(text => {{
    const rows = parseCSV(text);
    allRows = rows
      .map(r => {{
        const [a='',b='',c='',d='',e='',f=''] = r;
        return [a.trim(), b.trim(), c.trim(), d.trim(), e.trim(), f.trim()];
      }})
      .filter(r => r.some(Boolean));
    renderMenuGrouped(allRows);
    renderCategoryMenu(allRows);
    document.getElementById('noResults').style.display = allRows.length ? "none" : "block";
  }})
  .catch(err => {{
    console.error('Error CSV:', err);
    const el = document.getElementById("noResults");
    el.style.display = "block";
    el.textContent = "Error al cargar el menú.";
  }});


    fetch(FIJOS_URL)
      .then(r => r.text())
      .then(data => {{
        const rows = data.split("\\n").map(r => r.split(","));
        document.getElementById("nombre-resto").textContent    = rows[1]?.[1]?.replace(/"/g, "").trim() || "";
        document.getElementById("subtitulo-resto").textContent = rows[2]?.[1]?.replace(/"/g, "").trim() || "";
        document.getElementById("direccion-resto").textContent = rows[3]?.[1]?.replace(/"/g, "").trim() || "";
        document.getElementById("horarios-resto").textContent  = rows[4]?.[1]?.replace(/"/g, "").trim() || "";
        document.getElementById("banner-resto").src            = rows[5]?.[1]?.replace(/"/g, "").trim() || "";
        document.getElementById("whatsapp-float").href         = "https://wa.me/" + (rows[7]?.[1]?.replace(/"/g, "").trim() || "");
        const socialLinks = [
          {{
            href: rows[8]?.[1]?.replace(/"/g, "").trim() || "",
            img: "https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png",
            alt: "Instagram",
            label: "Instagram"
          }},
          {{
            href: rows[9]?.[1]?.replace(/"/g, "").trim() || "",
            img: "https://upload.wikimedia.org/wikipedia/commons/5/51/Facebook_f_logo_%282019%29.svg",
            alt: "Facebook",
            label: "Facebook"
          }},
          {{
            href: rows[10]?.[1]?.replace(/"/g, "").trim() || "",
            img: "https://res.cloudinary.com/drxznqm61/image/upload/v1752716379/rappi_oul48p.png",
            alt: "Rappi",
            label: "Rappi"
          }},
          {{
            href: rows[11]?.[1]?.replace(/"/g, "").trim() || "",
            img: "https://res.cloudinary.com/drxznqm61/image/upload/v1752716289/pedidosya_q40sz4.png",
            alt: "PedidosYa",
            label: "PedidosYa"
          }},
          {{
            href: rows[12]?.[1]?.replace(/"/g, "").trim() || "",
            img: "https://res.cloudinary.com/drxznqm61/image/upload/v1752716133/googlemaps-removebg-preview_xh3ivm.png",
            alt: "Google Maps",
            label: "Google Maps"
          }}
        ];

        const socialsDiv = document.getElementById('headerSocials');
        socialsDiv.innerHTML = "";
        socialLinks.forEach(social => {{
          if (social.href && social.href.trim() !== "") {{
            const a = document.createElement('a');
            a.href = social.href;
            a.target = "_blank";
            a.setAttribute('aria-label', social.label);
            const img = document.createElement('img');
            img.src = social.img;
            img.alt = social.alt;
            a.appendChild(img);
            socialsDiv.appendChild(a);
          }}
        }});
      }});

    const FONTS_URL =
      'https://script.google.com/macros/s/AKfycbyoUpJYVybiCQRpIoKTPH8uEDTbdzPWI9BcfCcQwUeitz8eXsQXx6MlFj-lsmGTcn4/exec?action=fonts&sheet_url=' +
      encodeURIComponent("{sheet_url}");

    // Aplica dinámicamente shorthand CSS (p. ej. "italic 1rem 'Poppins', sans-serif")
    fetch(FONTS_URL)
      .then(r => r.json())
      .then(({{ ok, vars }}) => {{
        if (!ok || !vars) return;
        Object.entries(vars).forEach(([cssVar, shorthand]) => {{
          document.documentElement.style.setProperty(cssVar, shorthand);
        }});
      }})
      .catch(err => console.error("Personalizacion FONTS error:", err));

    const COLORS_URL =
      'https://script.google.com/macros/s/AKfycbyoUpJYVybiCQRpIoKTPH8uEDTbdzPWI9BcfCcQwUeitz8eXsQXx6MlFj-lsmGTcn4/exec?action=colors&sheet_url=' +
      encodeURIComponent("{sheet_url}");

    fetch(COLORS_URL)
      .then(r => r.json())
      .then(({{ ok, vars }}) => {{
        if (!ok || !vars) return;
        Object.entries(vars).forEach(([cssVar, color]) => {{
          document.documentElement.style.setProperty(cssVar, color);
        }});
      }})
      .catch(err => console.error("Personalizacion BG error:", err));
  </script>
</body>
</html>
"""

with open(html_file, "w", encoding="utf-8") as f:
    f.write(html)

print("✅ HTML generado:", html_file)
print("📄 Planilla conectada:", sheet_url)

# === EXPORTAR PATHS PARA WORKFLOW
with open("menu_url.txt", "w") as f:
    f.write(f"planes/menu-corporativo-{fecha_id}-{hash_str}/index.html")
with open("sheet_url.txt", "w") as f:
    f.write(sheet_url)
