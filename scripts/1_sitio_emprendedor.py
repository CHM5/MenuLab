import os
import json
from pathlib import Path
from datetime import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# === CONFIG ===
TEMPLATE_SHEET_ID = "1bLzEXHmei95_XlHDBVO1sYHkDU5nEQwfLdCA8XCCoWo"
FIJOS_RANGE = "Datos Permanentes!B4:B15"
MENU_RANGE = "Menu!A2:E1000"
fecha_id = datetime.now().strftime("%Y%m%d-%H%M")

# === AUTENTICACIÓN ===
credentials_info = json.loads(os.environ["GOOGLE_CREDENTIALS"])
creds = Credentials.from_service_account_info(
    credentials_info,
    scopes=[
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/spreadsheets.readonly"
    ]
)

drive_service = build("drive", "v3", credentials=creds)
sheets_service = build("sheets", "v4", credentials=creds)

# === EXTERNAL_REFERENCE ===
external_ref = os.environ.get("EXTERNAL_REFERENCE")
if not external_ref:
    print("❌ EXTERNAL_REFERENCE no provisto en las variables de entorno")
    exit(1)

# === CLIENT EMAIL ===
client_email = os.environ.get("CLIENT_EMAIL", "default_email@example.com")

# === COPIAR PLANTILLA ===
try:
    copia = drive_service.files().copy(
        fileId=TEMPLATE_SHEET_ID,
        body={"name": f"Menu Emprendedor {fecha_id}"}
    ).execute()
    sheet_id = copia["id"]
    sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"
    print("🔗 CSV para menú en vivo:", csv_url)

    # Compartir con el cliente
    drive_service.permissions().create(
        fileId=sheet_id,
        body={
            'type': 'user',
            'role': 'writer',
            'emailAddress': client_email
        }
    ).execute()

    drive_service.permissions().create(
        fileId=sheet_id,
        body={
            'type': 'anyone',
            'role': 'reader'
        },
        sendNotificationEmail=False
    ).execute()

except HttpError as e:
    print(f"❌ Error al copiar o compartir la planilla: {e}")
    exit(1)

# === LEER DATOS FIJOS + MENÚ (opcional, si se quiere procesar algo) ===
try:
    fijos_result = sheets_service.spreadsheets().values().get(
        spreadsheetId=sheet_id,
        range=FIJOS_RANGE
    ).execute()
    fijos_rows = fijos_result.get("values", [])

    menu_result = sheets_service.spreadsheets().values().get(
        spreadsheetId=sheet_id,
        range=MENU_RANGE
    ).execute()
    menu_rows = menu_result.get("values", [])

except Exception as e:
    print(f"❌ Error al leer datos de la planilla: {e}")
    fijos_rows = []
    menu_rows = []

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
  <style>
    body {{
      font-family: 'Segoe UI', Arial, sans-serif;
      background: #fff;
      color: #212529;
      margin: 0;
      padding: 0;
    }}
    .container {{
      max-width: 900px;
      margin: 0 auto;
      padding: 1rem;
    }}
    /* Agregá el resto de los estilos como en los ejemplos previos */
  </style>
</head>
<body>
  <header>
    <h1>Menú Online</h1>
  </header>
  <div class="container">
    <div id="menuTable"></div>
  </div>
  <script>
    const CSV_URL = "{csv_url}";
    fetch(CSV_URL)
      .then(response => response.text())
      .then(data => {{
        // Procesar CSV en frontend si querés
        console.log("✅ Menú cargado");
      }})
      .catch(err => {{
        console.error("❌ Error cargando el menú:", err);
      }});
  </script>
</body>
</html>
"""

with open(html_file, "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Menú generado:", html_file)
print("📄 Planilla editable:", sheet_url)

# === EXPORTAR PARA EL WORKFLOW ===
with open("menu_url.txt", "w") as f:
    f.write(f"planes/menu-emprendedor-{fecha_id}/index.html")

with open("sheet_url.txt", "w") as f:
    f.write(sheet_url)

with open("external_ref.txt", "w") as f:
    f.write(external_ref)
