import os
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# === CONFIGURACIÓN ===
SHEET_URL = os.environ.get("SHEET_URL")
if not SHEET_URL:
    print("❌ Falta SHEET_URL en variables de entorno.")
    exit(1)

sheet_id = SHEET_URL.split("/d/")[1].split("/")[0]
RANGO_TEST = "Menu!A1:E1"  # leer 2 celdas como prueba

# === CARGAR CREDENCIALES ===
try:
    credentials_info = json.loads(os.environ["GOOGLE_CREDENTIALS"])
    creds = Credentials.from_service_account_info(
        credentials_info,
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
except Exception as e:
    print(f"❌ Error al cargar credenciales: {e}")
    exit(1)

# === CREAR CLIENTE Y LEER ===
try:
    service = build("sheets", "v4", credentials=creds)
    result = service.spreadsheets().values().get(
        spreadsheetId=sheet_id,
        range=RANGO_TEST
    ).execute()
    values = result.get("values", [])

    print("✅ Acceso verificado. Datos recibidos:")
    for row in values:
        print("  ", row)

except Exception as e:
    print(f"❌ Error al acceder a la hoja: {e}")
    exit(1)