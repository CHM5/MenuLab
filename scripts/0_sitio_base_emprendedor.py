import os
import json
from pathlib import Path
from datetime import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# === CONFIGURACIÓN ===
MENU_RANGE = "Menu!A2:E"
FIJOS_RANGE = "Datos Fijos!C3:C6"
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

sheet_id = sheet_url.split("/d/")[1].split("/")[0]
csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"
fijos_csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Datos%20Fijos"

# === VALIDAR CONEXIÓN (opcional)
try:
    sheets_service.spreadsheets().values().get(spreadsheetId=sheet_id, range=MENU_RANGE).execute()
    print("✅ Conexión con Google Sheets verificada.")
except Exception as e:
    print(f"⚠️ Advertencia: no se pudo validar conexión con Sheets: {e}")

# === GENERAR HTML ===
output_dir = Path(f"planes/menu-emprendedor-{fecha_id}")
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
      --primary: #ffc107;
      --bg: #f1f1f1;
      --text: #212529;
      --header: #d2d0cd;
      --border: #dee2e6;
      --radius: 10px;
    }}
    body {{
      font-family: 'Segoe UI', Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
      margin: 0;
      padding: 0;
    }}
    header {{
      background: var(--header);
      color: #000;
      padding: 0.8rem 1rem 0.5rem 1rem;
      border-radius: 0 0 var(--radius) var(--radius);
    }}
    .container {{
      max-width: 900px;
      margin: 0 auto;
      padding: 1rem;
    }}
    .search-menu {{
      text-align: center;
      margin: 1rem 0;
      position: sticky;
      top: 0;
      padding-top: 8px;
    }}
    .search-menu input {{
      padding: 0.5rem 1rem;
      border-radius: 20px;
      border: 1px solid #ccc;
      width: 90%;
      max-width: 400px;
      font-size: 1rem;
    }}
    .category-menu {{
      display: flex;
      gap: 12px;
      justify-content: center;
      align-items: center;
      margin-bottom: 0.5rem;
      flex-wrap: nowrap;
      overflow-x: auto;
      padding: 8px 0;
      position: sticky;
      top: 50px;
      z-index: 1000;
      background: #f1f1f1;
    }}
    .category-btn {{
      background: #457B9D;
      color: #fff;
      border: none;
      border-radius: 20px;
      padding: 7px 18px;
      font-weight: 600;
      cursor: pointer;
      font-size: 1rem;
      transition: background 0.2s;
      flex: 0 0 auto;
    }}
    .category-btn:hover, .category-btn.active {{ background: #457B9D; }}
    .menu-group {{ margin-top: 0.5rem; margin-bottom: 1.2rem; }}
    .menu-group h2 {{ font-size: 1.7rem; margin: 2rem 0 0.2rem; border-bottom: 2px solid #ddd; color: #333; }}
    .menu-group h3 {{ font-size: 1.5rem; margin: 1rem 0 0rem; color: #555; }}
    .menu-item {{ border-bottom: 1px solid #eee; margin: -.5rem 0 -.5rem; padding: 0.8rem 0; }}
    .menu-item-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0 0.5rem;
    }}
    .menu-name {{
      font-size: 1.1rem;
      margin: 0;
      font-weight: 600;
    }}
    .menu-price {{
      font-size: 1.1rem;
      font-weight: 500;
      color: #111;
    }}
    .menu-description {{
      margin: 0.2rem 0 0 0;
      font-size: 0.95rem;
      color: #666;
      padding: 0 1rem;
    }}
    .menu-content {{ margin-top: 2rem; }}
    footer {{
      background:#f1f1f1;
      color:#333;
      text-align:center;
      padding:1rem 0 1.2rem 0;
      font-size:1rem;
    }}
  </style>
</head>
<body>
  <header>
    <img src="https://res.cloudinary.com/drxznqm61/image/upload/v1752632048/cafe-central_ne83eh.png" alt="Banner" style="width:100%;display:block;margin-bottom:0.5rem;">
    <div class="container">
      <h1 id="nombre-resto"></h1>
      <h2 id="subtitulo-resto" style="font-style:italic;"></h2>
      <div>
        <span id="direccion-resto"></span> - <span id="horarios-resto"></span>
      </div>
    </div>
  </header>
  <div class="search-menu">
    <input id="menuSearch" type="text" placeholder="Buscar en la carta..." />
  </div>
  <div id="categoryMenu" class="category-menu"></div>
  <div class="container">
    <div id="menuTable" class="menu-content"></div>
    <div id="noResults" style="display:none;text-align:center;color:#dc3545;margin-top:1.5rem;font-size:1.1rem;">
      No se encontraron platos con ese criterio.
    </div>
  </div>
  <footer>
    <span class="thq-body-small">Desarrollado por</span>
    <a href="https://menulab.com.ar" target="_blank" rel="noopener">
      <h1 style="font-family:'Unbounded',sans-serif;font-weight:600;font-size:100%;margin-left:-10px;
          background:linear-gradient(90deg,#E639A6,#457B9D);
          -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
        MenuLab
      </h1>
    </a>
  </footer>
  <script>
    const CSV_URL = "{csv_url}";
    const FIJOS_URL = "{fijos_csv_url}";
    let allRows = [];

    function renderCategoryMenu(rows) {{
      const categories = [...new Set(rows.map(r => r[0]?.trim()).filter(Boolean))];
      const menuDiv = document.getElementById('categoryMenu');
      menuDiv.innerHTML = '';
      categories.forEach(cat => {{
        const btn = document.createElement('button');
        btn.className = 'category-btn';
        btn.textContent = cat;
        btn.onclick = () => {{
          const section = document.querySelector(`.menu-group[data-cat="${{cat}}"]`);
          if (section) section.scrollIntoView({{ behavior: 'smooth' }});
          document.querySelectorAll('.category-btn').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
        }};
        menuDiv.scrollLeft = 0;
        menuDiv.appendChild(btn);
      }});
    }}

    function renderMenuGrouped(rows) {{
      const container = document.getElementById("menuTable");
      container.innerHTML = "";
      const grouped = {{}};
      rows.forEach(cols => {{
        const [cat, subcat, name, desc, price] = cols.map(c => c.trim());
        if (!cat || !name) return;
        if (!grouped[cat]) grouped[cat] = {{}};
        const sub = subcat || "-";
        if (!grouped[cat][sub]) grouped[cat][sub] = [];
        grouped[cat][sub].push({{ name, desc, price }});
      }});
      Object.entries(grouped).forEach(([cat, subcats]) => {{
        const group = document.createElement("div");
        group.className = "menu-group";
        group.setAttribute("data-cat", cat);
        group.innerHTML = `<h2>${{cat}}</h2>`;
        Object.entries(subcats).forEach(([sub, items]) => {{
          if (sub !== "-") group.innerHTML += `<h3>${{sub}}</h3>`;
          items.forEach(item => {{
            group.innerHTML += `
              <div class="menu-item">
                <div class="menu-item-header">
                  <h4 class="menu-name">${{item.name}}</h4>
                  <span class="menu-price">${{item.price}}</span>
                </div>
                <p class="menu-description">${{item.desc}}</p>
              </div>`;
          }});
        }});
        container.appendChild(group);
      }});
    }}

    function filterMenuRows(rows, query) {{
      const q = query.toLowerCase();
      return rows.filter(r => r.some(c => c.toLowerCase().includes(q)));
    }}

    document.getElementById("menuSearch").addEventListener("input", function() {{
      const filtered = filterMenuRows(allRows, this.value);
      renderMenuGrouped(filtered);
      renderCategoryMenu(filtered);
      document.getElementById("noResults").style.display = filtered.length === 0 ? "block" : "none";
    }});

    fetch(CSV_URL).then(r => r.text()).then(data => {{
      allRows = data.split("\\n").slice(1).map(r => r.split(",").map(c => c.replace(/\"/g, "")));
      renderMenuGrouped(allRows);
      renderCategoryMenu(allRows);
    }});

    fetch(FIJOS_URL).then(r => r.text()).then(data => {{
      const rows = data.split("\\n").map(r => r.split(","));
      document.getElementById("nombre-resto").textContent = rows[0]?.[0] || "";
      document.getElementById("subtitulo-resto").textContent = rows[1]?.[0] || "";
      document.getElementById("direccion-resto").textContent = rows[2]?.[0] || "";
      document.getElementById("horarios-resto").textContent = rows[3]?.[0] || "";
    }});
  </script>
</body>
</html>
"""

with open(html_file, "w", encoding="utf-8") as f:
    f.write(html)

# Exportar rutas para otros procesos
with open("menu_url.txt", "w") as f:
    f.write(str(html_file))
with open("sheet_url.txt", "w") as f:
    f.write(sheet_url)
