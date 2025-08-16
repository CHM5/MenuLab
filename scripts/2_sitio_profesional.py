import os
import json
from pathlib import Path
from datetime import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import hashlib

# === CONFIGURACIÓN ===
MENU_RANGE = "Menu!A2:E26"
FIJOS_RANGE = "Datos Permanentes!B2:B14"
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
fijos_csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Datos%20Permanentes"
personalizacion_csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Personalizacion"

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

# === OBTENER COLORES DE PERSONALIZACION ===
def rgb_to_hex(rgb):
    if not rgb:
        return "#ffffff"
    r = int(rgb.get("red", 1) * 255)
    g = int(rgb.get("green", 1) * 255)
    b = int(rgb.get("blue", 1) * 255)
    return f"#{r:02x}{g:02x}{b:02x}"

# Mapeo: variable CSS -> fila en Personalizacion (0-indexed)
css_map = [
    ("--bg", 0),             # Fondo
    ("--header", 1),         # Encabezado
    ("--bgScrollbar", 2),    # Fondo Categorías
    ("--textScrollbar", 3),  # Texto Categorías
    ("--title", 4),          # Categoría
    ("--subtitle", 5),       # Subcategoría
    ("--plate", 6),          # Plato
    ("--description", 7),    # Descripción
    ("--price", 8),          # Precio
]

personalizacion_colors = {}

try:
    sheet = sheets_service.spreadsheets().get(
        spreadsheetId=sheet_id,
        ranges=["Personalizacion!C2:C10"],
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
        "--bg": "#f1f1f1",
        "--header": "#212529",
        "--bgScrollbar": "#457B9D",
        "--textScrollbar": "#fff",
        "--title": "#333",
        "--subtitle": "#555",
        "--plate": "#555",
        "--description": "#666",
        "--price": "#111"
    }

# === GENERAR HTML ===
# Generar hash único de 5 dígitos usando la fecha y la URL de la planilla
hash_input = f"{fecha_id}-{sheet_url}".encode("utf-8")
hash_str = hashlib.sha1(hash_input).hexdigest()[:5]

output_dir = Path(f"planes/menu-profesional-{fecha_id}-{hash_str}")
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
      --bg: {personalizacion_colors['--bg']};
      --header: {personalizacion_colors['--header']};
      --bgScrollbar: {personalizacion_colors['--bgScrollbar']};
      --textScrollbar: {personalizacion_colors['--textScrollbar']};
      --title: {personalizacion_colors['--title']};
      --subtitle: {personalizacion_colors['--subtitle']};
      --plate: {personalizacion_colors['--plate']};
      --description: {personalizacion_colors['--description']};
      --price: {personalizacion_colors['--price']};
      --radius: 10px;
    }}
    body {{
      font-family: 'Segoe UI', Arial, sans-serif;
      background: var(--bg);
      color: var(--bg);
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
      font-size: 1.7rem;
      margin: 2rem 0 0.2rem;
      border-bottom: 2px solid #ddd;
      color: var(--title); /* Color del título de la categoría #333 */
    }}
    .menu-group h3 {{
      font-size: 1.5rem;
      margin: 1rem 0 0rem;
      color: var(--subtitle); /* Color del subtítulo de la categoría #555 */
    }}
    .menu-group h4 {{
      font-size: 1.2rem;
      margin: 1rem 0 0rem;
      color: var(--plate); /* Color del nombre del plato #555 */
    }}
    .menu-description {{
      margin: 0.2rem 0 0 0;
      font-size: 0.95rem;
      color: var(--description); /* Color de la descripción del plato #666 */
      padding: 0 1rem;
    }}
    .menu-price {{
      font-size: 1.1rem;
      font-weight: 500;
      color: var(--price); /* Color del precio  #111*/
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
      margin: -10000px 0 0.5rem 0;
      flex-wrap: nowrap;
      overflow-x: auto;
      padding-top: 8px;
      padding-bottom: 8px;
      scrollbar-width: thin;
      scrollbar-color: var(--bgScrollbar) #eee;
      position: sticky;
      top: 50px;
      z-index: 1000;
      background: #457B9D;
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
      background: var(--bgScrollbar);
      color: var(--textScrollbar);
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
      color: var(--header);
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
        background-color: #f1f1f1; /* gris clarito */
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
    .style-nombre {{
      font-size:1.8rem;
      color:var(--header); 
      margin-bottom:0; 
      margin-top:0;
    }}
    .style-subtitulo {{
      margin:0.2rem 0 0.3rem 0;
      font-size:1rem;
      font-weight:400;
      color:var(--header);
      font-style:italic;
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
        <div><span id="direccion-resto"></span></div>
        <div><span id="horarios-resto"></span></div>
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
  <script>
    const CSV_URL = "{csv_url}";
    const FIJOS_URL = "{fijos_csv_url}";
    const PERSONALIZACION_URL = "{personalizacion_csv_url}";

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
                <span class="menu-price">$${{item.precio}}</span>
              </div>
              <p class="menu-description">${{item.desc}}</p>
            `;
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

    let allRows = [];
    fetch(CSV_URL)
      .then(r => r.text())
      .then(data => {{
        allRows = data.split("\\n").slice(1).map(r => r.split(",").map(c => c.replace(/\"/g, "")));
        renderMenuGrouped(allRows);
        renderCategoryMenu(allRows);
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

    // Mapea el nombre de la fila (columna B) a tu variable CSS
    const VAR_MAP = {{
      "Fondo": "--bg",
      "Encabezado": "--header",
      "Fondo Categorías": "--bgScrollbar",
      "Texto Categorías": "--textScrollbar",
      "Categoría": "--title",
      "Subcategoría": "--subtitle",
      "Plato": "--plate",
      "Descripción": "--description",
      "Precio": "--price"
    }};

  // Lee la hoja y setea variables (B = nombre, C = color)
  fetch(PERSONALIZACION_URL)
    .then(r => r.text())
    .then(csv => {{
      const rows = csv.trim().split(/\r?\n/).map(r => r.split(","));
      // salteo encabezado: “Fuente,Color”
      rows.slice(1).forEach(cols => {{
        const nombre = (cols[1] || "").replace(/"/g, "").trim(); // col B
        const color  = (cols[2] || "").replace(/"/g, "").trim(); // col C
        const varCSS = VAR_MAP[nombre];
        if (varCSS && color) {{
          document.documentElement.style.setProperty(varCSS, color);
        }}
      }});
    }})
    .catch(err => console.error("Error Personalizacion:", err));

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
    f.write(f"planes/menu-profesional-{fecha_id}-{hash_str}/index.html")
with open("sheet_url.txt", "w") as f:
    f.write(sheet_url)
