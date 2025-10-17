from pathlib import Path
import os, json, re
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# === CONFIGURACIÓN ===
TEMPLATE_HTML = Path("templates/emprendedor.html")
CSS_FILE = Path("templates/emprendedor.css")
JS_FILE = Path("templates/emprendedor.js")

# === AUTENTICACIÓN ===
credentials_info = json.loads(os.environ["GOOGLE_CREDENTIALS"])
creds = Credentials.from_service_account_info(credentials_info, scopes=["https://www.googleapis.com/auth/spreadsheets"])
sheets_service = build("sheets", "v4", credentials=creds)

# === DATOS DEL NEGOCIO ===
restaurant_name = os.environ.get("NEGOCIO", "Restaurante").strip()
sheet_url = os.environ["SHEET_URL"]
sheet_id = sheet_url.split("/d/")[1].split("/")[0]
slug = re.sub(r'[^a-zA-Z0-9]+', '-', restaurant_name.lower()).strip('-')

# === URLs ===
csv_menu = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Menu"
csv_fijos = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Datos"

# === CARGAR ARCHIVOS ===
html_template = TEMPLATE_HTML.read_text(encoding="utf-8")
css_content = CSS_FILE.read_text(encoding="utf-8")
js_content = JS_FILE.read_text(encoding="utf-8")

# === REEMPLAZOS ===
final_html = (
    html_template
    .replace("{{RESTAURANTE}}", restaurant_name)
    .replace("{{CSV_MENU}}", csv_menu)
    .replace("{{CSV_FIJOS}}", csv_fijos)
    .replace("{{CSS_EMPRENDEDOR}}", css_content)
    .replace("{{JS_EMPRENDEDOR}}", js_content)
    .replace("{{TOP_MENU}}", "<button id='printBtn' onclick='window.print()'>🖨️ Vista Previa</button>")
)

# === GUARDAR ===
output_dir = Path(f"menu/{slug}")
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / "index.html"
output_file.write_text(final_html, encoding="utf-8")

print(f"✅ Menú Emprendedor generado: {output_file}")
print(f"🌐 URL pública: https://menulab.com.ar/menu/{slug}/")
