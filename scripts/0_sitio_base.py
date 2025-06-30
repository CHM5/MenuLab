import os
import json
from pathlib import Path
from datetime import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# === CONFIG ===
TEMPLATE_SHEET_ID = "12rwhH-LQ5S5R8UjNr-P422_U03imcIJAP4xIwD5Q3CY"
FIJOS_RANGE = "Datos Permanentes!B4:B15"
SHEET_FIELDS = ["Categoría", "Subcategoría", "Nombre", "Descripción", "Precio"]
MENU_RANGE = "Carta!A2:E26"  # Hasta 25 productos

# === AUTENTICACIÓN ===
credentials_info = json.loads(os.environ["GOOGLE_CREDENTIALS"])
creds = Credentials.from_service_account_info(
    credentials_info,
    scopes=["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/spreadsheets"]
)

drive_service = build("drive", "v3", credentials=creds)
sheets_service = build("sheets", "v4", credentials=creds)

# === GENERAR NOMBRE Y COPIAR SHEET ===
fecha_id = datetime.now().strftime("%Y%m%d-%H%M")
nombre_copia = f"Menu Base {fecha_id}"

copia = drive_service.files().copy(
    fileId=TEMPLATE_SHEET_ID,
    body={"name": nombre_copia}
).execute()

sheet_id = copia["id"]  # 👈 ESTA LÍNEA ES CLAVE
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"
csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"
print("🔗 CSV para menú en vivo:", csv_url)

# === LEER EL CORREO DEL CLIENTE ===
cliente_email = os.environ.get("CLIENT_EMAIL", "default_email@example.com")  # Usando una variable de entorno o pasando por el flujo de GitHub

# Si el correo no es pasado por el entorno, puedes también tomarlo directamente de la variable del flujo
cliente_email = cliente_email or "default_email@example.com"  # Aquí usas el email pasado por el flujo si está disponible

# === DAR PERMISOS DE EDICIÓN AL CLIENTE ===
def share_sheet_with_client(sheet_id, client_email):
    try:
        # Crear el servicio de Drive
        service = build('drive', 'v3', credentials=creds)

        # Llamada para otorgar permisos de edición al cliente
        permission = {
            'type': 'user',
            'role': 'writer',  # 'writer' para permisos de edición
            'emailAddress': client_email
        }

        # Crear el permiso
        service.permissions().create(
            fileId=sheet_id,
            body=permission
        ).execute()

        print(f"Se ha dado acceso de escritura a: {client_email}")

    except HttpError as error:
        print(f'Ha ocurrido un error al compartir el archivo: {error}')
# Llamada a la función para compartir el sheet con el cliente
share_sheet_with_client(sheet_id, cliente_email)

# Permiso general: cualquiera con el enlace puede ver
drive_service.permissions().create(
    fileId=sheet_id,
    body={
        "type": "anyone",
        "role": "reader"
    },
    sendNotificationEmail=False
).execute()

# Leer datos fijos
fijos_result = sheets_service.spreadsheets().values().get(
    spreadsheetId=sheet_id,
    range=FIJOS_RANGE
).execute()
fijos_rows = fijos_result.get("values", [])

# Leer menú
menu_result = sheets_service.spreadsheets().values().get(
    spreadsheetId=sheet_id,
    range=MENU_RANGE
).execute()
menu_rows = menu_result.get("values", [])


# Opcional: convertir datos fijos a una lista simple (quita sublistas vacías)
fijos = [row[0] for row in fijos_rows if row]

# === GENERAR HTML RESPONSIVO CON BUSCADOR ===
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
      font-size: 1.5rem;
      margin: 0.3rem 0 0.2rem;
      border-bottom: 2px solid #ddd;
      color: #333;
    }}

    .menu-group h3 {{
      font-size: 1.2rem;
      margin-top: 0.6rem;
      color: #555;
    }}

    .menu-item {{
      border-bottom: 1px solid #eee;
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
      <div id="menuTable" class="menu-content"></div>
    </div>
    <div id="noResults" style="display:none;text-align:center;color:#dc3545;margin-top:1.5rem;font-size:1.1rem;">
      No se encontraron platos con ese criterio.
    </div>
  </div>
  <footer style="background:#f1f1f1;color:#333;text-align:center;padding:1rem 0 1.2rem 0;font-size:1rem;">
    <div>
      <span>Dirección: </span>
      <span id="direccion-resto" style="font-weight: bold;"></span>
    </div>
    <div>
      <span>Horarios: </span>
      <span id="horarios-resto" style="font-weight: bold;"></span>
    </div>
    <a href="https://menulab.com.ar" target="_blank" rel="noopener">
      <span class="thq-body-small">En colaboración con:</span>  
      <span style="display: inline-block; margin-left: 12px;">
        <h1 style="
          font-family: 'Unbounded', sans-serif;
          font-weight: 600;
          font-size: 100%;
          margin: 0;
          background: linear-gradient(90deg, #E639A6, #457B9D); /* azul al rosa */
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;">
          MenuLab
        </h1>
      </span>
    </a>
  </footer>

  <script>
    const CSV_URL = "{csv_url}";
    let allRows = [];

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
      .then(response => response.text())
      .then(data => {{
        allRows = data.split("\\n").slice(1, 26).map(row =>
          row.split(",").map(col => col.replace(/\"/g, ""))
        );
        renderMenuGrouped(allRows);
      }})
      .catch(err => {{
        document.getElementById("noResults").style.display = "block";
        document.getElementById("noResults").textContent = "Error al cargar el menú.";
        console.error("Error al cargar el CSV:", err);
      }});

    // Cargar Valores Estaticos en vivo
    const STATIC_CSV_URL = "{sheet_url.replace('/edit', '')}/gviz/tq?tqx=out:csv&sheet=Datos%20Fijos";
    fetch(STATIC_CSV_URL)
      .then(response => response.text())
      .then(data => {{
        const rows = data.split("\\n").map(row => row.split(","));

        const nombre = (rows[2] && rows[2][2]) ? rows[2][2].replace(/"/g, "").trim() : "";
        if (nombre) {{
          document.getElementById("nombre-resto").textContent = nombre;
        }}

        const subtitulo = (rows[3] && rows[3][2]) ? rows[3][2].replace(/"/g, "").trim() : "";
        if (subtitulo) {{
          document.getElementById("subtitulo-resto").textContent = subtitulo;
        }}
                
        const direccion = (rows[4] && rows[4][2]) ? rows[4][2].replace(/"/g, "").trim() : "";
        if (direccion) {{
          document.getElementById("direccion-resto").textContent = direccion;
        }}

        const horarios = (rows[5] && rows[5][2]) ? rows[5][2].replace(/"/g, "").trim() : "";
        if (horarios) {{
          document.getElementById("horarios-resto").textContent = horarios;
        }}
      }});

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
                  <h3 class="menu-name">${{item.nombre}}</h3>
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


  </script>
</body>
</html>
"""

with open(html_file, "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Menú generado:", html_file)
print("📄 Planilla editable:", sheet_url)

# NUEVO → exportar urls para el workflow
with open("menu_url.txt", "w") as f:
    # ruta pública en GitHub Pages
    f.write(f"planes/menu-base-{fecha_id}/index.html")

with open("sheet_url.txt", "w") as f:
    f.write(sheet_url)