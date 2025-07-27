import os
import json
from pathlib import Path
from datetime import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# === CONFIGURACIÓN ===
MENU_RANGE = "Carta!A2:E26"
FIJOS_RANGE = "Datos Permanentes!B2:B5"
fecha_id = datetime.now().strftime("%Y%m%d-%H%M")

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
csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"
fijos_csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Datos%20Permanentes"
print("🔗 CSV menú:", csv_url)
print("🔗 CSV fijos:", fijos_csv_url)

# === VALIDAR CONEXIÓN (sin cortar si falla) ===
try:
    sheets_service.spreadsheets().values().get(
        spreadsheetId=sheet_id, range=MENU_RANGE
    ).execute()
    print("✅ Conexión con Google Sheets verificada.")
except Exception as e:
    print(f"⚠️ Advertencia: no se pudo validar conexión con Sheets: {e}")

# === GENERAR HTML ===
output_dir = Path(f"planes/menu-base-{fecha_id}")
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
    .menu-group {{
      margin-top: 0.5rem;
      margin-bottom: 1.2rem;
    }}
    .menu-group h2 {{
      font-size: 1.7rem;
      margin: 2rem 0 0.2rem;
      border-bottom: 2px solid #ddd;
      color: #333;
    }}
    .menu-group h3 {{
      font-size: 1.5rem;
      margin: 1rem 0 0rem;
      color: #555;
    }}
    .menu-group h4 {{
      font-size: 1.2rem;
      margin: 1rem 0 0rem;
      color: #555;
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
    .menu-content {{
      margin-top: 2rem;
    }}
    .category-menu {{
      display: flex;
      gap: 12px;
      justify-content: center;
      align-items: center;
      margin: -10000px 0 0.5rem 0;
      flex-wrap: nowrap;
      overflow-x: auto;
      padding-top: 8px;
      padding-bottom: 8px;
      scrollbar-width: thin;
      scrollbar-color: #457B9D #eee;
      position: sticky;
      top: 0;
      z-index: 1000;
      background: var(--bg);
    }}
    .category-menu::-webkit-scrollbar {{
      height: 6px;
    }}
    .category-menu::-webkit-scrollbar-thumb {{
      background: #457B9D;
      border-radius: 10px;
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
      color:#000;
      font: italic 0.9rem 'Segoe UI', sans-serif;
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
  </style>
</head>
<body>
  <header>
    <div class="container">
      <a href="https://menulab.com.ar" target="_blank" rel="noopener">
        <img src="https://res.cloudinary.com/drxznqm61/image/upload/v1750637502/BannerMenuLab_mbtrzh.jpg" alt="Banner MenuLab" style="width:100%;display:block;margin-bottom:0.5rem;">
      </a>
      <div class="header-flex">
        <div class="header-left">
          <h1 id="nombre-resto" style="font-size:1.8rem; margin:0;"></h1>
          <h2 id="subtitulo-resto" style="margin:0.2rem 0 0.3rem 0;font-size:1rem;font-weight:400;font-style:italic;"></h2>
        </div>
        <div class="header-right">
          <div><span id="direccion-resto"> </span></div>
          <div><span id="horarios-resto"> </span></div>
        </div>
      </div>
    </div>
  </header>

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
        <h1 style="
          font-family: 'Unbounded', sans-serif;
          font-weight: 600;
          font-size: 100%;
          margin-left: -10px;
          background: linear-gradient(90deg, #E639A6, #457B9D);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;">
          MenuLab
        </h1>
      </span>
    </a>
  </footer>

  <script>
    const CSV_URL = "{csv_url}";
    const FIJOS_URL = "{fijos_csv_url}";

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
        const [cat, subcat, nombre, desc, precio] = cols.map(c => c.trim());
        if (!cat || !nombre) return;

        if (!agrupado[cat]) agrupado[cat] = {{}};
        const sub = subcat || "-";
        if (!agrupado[cat][sub]) agrupado[cat][sub] = [];
        agrupado[cat][sub].push({{ nombre, desc, precio }});
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
            itemDiv.innerHTML = `
              <div class="menu-item-header">
                <h4 class="menu-name">${{item.nombre}}</h4>
                <span class="menu-price">${{item.precio}}</span>
              </div>
              <p class="menu-description">${{item.desc}}</p>
            `;
            group.appendChild(itemDiv);
          }});
        }});

        container.appendChild(group);
      }});
    }}

    fetch(CSV_URL)
      .then(r => r.text())
      .then(data => {{
        const rows = data.split("\\n").slice(1).map(r => r.split(",").map(c => c.replace(/\"/g, "")));
        renderMenuGrouped(rows);
        renderCategoryMenu(rows);
      }})
      .catch(err => {{
        document.getElementById("noResults").style.display = "block";
        document.getElementById("noResults").textContent = "Error al cargar el menú.";
      }});

    fetch(FIJOS_URL)
      .then(r => r.text())
      .then(data => {{
        const rows = data.split("\\n").map(r => r.split(","));
        document.getElementById("nombre-resto").textContent    = rows[1]?.[1]?.replace(/"/g, "").trim() || "";
        document.getElementById("subtitulo-resto").textContent = rows[2]?.[1]?.replace(/"/g, "").trim() || "";
        document.getElementById("direccion-resto").textContent = rows[3]?.[1]?.replace(/"/g, "").trim() || "";
        document.getElementById("horarios-resto").textContent  = rows[4]?.[1]?.replace(/"/g, "").trim() || "";
      }});
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
    f.write(f"planes/menu-base-{fecha_id}/index.html")
with open("sheet_url.txt", "w") as f:
    f.write(sheet_url)
