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

# URLs para CSV
csv_url = f"{sheet_url.replace('/edit', '')}/gviz/tq?tqx=out:csv"
fijos_csv_url = f"{sheet_url.replace('/edit', '')}/gviz/tq?tqx=out:csv&sheet=Datos%20Permanentes"
print("🔗 CSV menú:", csv_url)
print("🔗 CSV fijos:", fijos_csv_url)

# === LEER DATOS DE PRUEBA (opcional, para validar conexión) ===
try:
    sheet_id = sheet_url.split("/d/")[1].split("/")[0]
    sheets_service.spreadsheets().values().get(
        spreadsheetId=sheet_id, range=MENU_RANGE
    ).execute()
except Exception as e:
    print(f"❌ Error al leer datos: {e}")
    exit(1)

# === CREAR HTML ===
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
  <style>
    :root {{
      --primary: #ffc107;
      --bg: #fff;
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
    .search-box {{
      display: flex;
      align-items: center;
      margin-bottom: 1.2rem;
      background: #f8f9fa;
      border-radius: var(--radius);
      padding: 0.5rem 1rem;
      box-shadow: 0 2px 8px #0001;
    }}
    .search-box input {{
      flex: 1;
      border: none;
      background: transparent;
      font-size: 1.1rem;
      padding: 0.7rem 0.5rem;
      outline: none;
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
      border-bottom: 1px solid var(--border);
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
  </style>
</head>
<body>
  <header>
    <a href="https://menulab.com.ar" target="_blank" rel="noopener">
      <img src="https://res.cloudinary.com/drxznqm61/image/upload/v1750637502/BannerMenuLab_mbtrzh.jpg" alt="Banner MenuLab" style="width:100%;display:block;margin-bottom:0.5rem;">
    </a>
    <h1 id="nombre-resto" style="font-size:2rem; color:#000;">Menú Online</h1>
    <h2 id="subtitulo-resto" style="margin:0.2rem 0 0.7rem 0;font-size:1.2rem;font-weight:400;color:#000;"></h2>
  </header>
  <div class="container">
    <div style="overflow-x:auto;">
      <table id="menuTable">
        <thead>
          <tr>
            <th>Categoría</th>
            <th>Subcategoría</th>
            <th>Nombre</th>
            <th>Descripción</th>
            <th>Precio</th>
          </tr>
        </thead>
        <tbody></tbody>
      </table>
    </div>
    <div id="noResults" style="display:none;text-align:center;color:#dc3545;margin-top:1.5rem;font-size:1.1rem;">
      No se encontraron platos con ese criterio.
    </div>
  </div>
  <footer style="background:#f1f1f1;color:#333;text-align:center;padding:1rem 0 1.2rem 0;font-size:1rem;">
    <div><span>Dirección: </span><span id="direccion-resto" style="font-weight: bold;"></span></div>
    <div><span>Horarios: </span><span id="horarios-resto" style="font-weight: bold;"></span></div>
    <a href="https://menulab.com.ar" target="_blank" rel="noopener">
      <span class="thq-body-small">En colaboración con:</span>
      <span style="display: inline-block; margin-left: 12px;">
        <h1 style="
          font-family: 'Unbounded', sans-serif;
          font-weight: 600;
          font-size: 100%;
          margin: 0;
          background: linear-gradient(90deg, #E639A6, #457B9D);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;">MenuLab</h1>
      </span>
    </a>
  </footer>

  <script>
    const CSV_URL = "{csv_url}";
    const FIJOS_URL = "{fijos_csv_url}";

    function renderTable(rows) {{
      const tbody = document.querySelector("#menuTable tbody");
      tbody.innerHTML = "";
      let count = 0;
      rows.forEach(cols => {{
        if (cols.length >= 3 && cols.some(cell => cell.trim() !== "")) {{
          const tr = document.createElement("tr");
          cols.slice(0, 5).forEach(cell => {{
            const td = document.createElement("td");
            td.textContent = cell;
            tr.appendChild(td);
          }});
          tbody.appendChild(tr);
          count++;
        }}
      }});
      document.getElementById("noResults").style.display = count === 0 ? "block" : "none";
    }}

    fetch(CSV_URL)
      .then(r => r.text())
      .then(data => {{
        const rows = data.split("\\n").slice(1).map(r => r.split(",").map(c => c.replace(/\"/g, "")));
        renderTable(rows);
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

# === EXPORTAR PATHS PARA WORKFLOW (opcional)
with open("menu_url.txt", "w") as f:
    f.write(f"planes/menu-base-{fecha_id}/index.html")
with open("sheet_url.txt", "w") as f:
    f.write(sheet_url)
