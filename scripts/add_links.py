import os
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# === CONFIG ===
CLIENTS_SHEET_ID = "1-9h8RaRXEbgZ_adYQWoAGqDT3t3kMt9pnyjgV_bYzBw"
SHEET_NAME = "Clientes"

# === AUTENTICACIÓN ===
credentials_info = json.loads(os.environ["GOOGLE_CREDENTIALS"])
creds = Credentials.from_service_account_info(
    credentials_info,
    scopes=["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/spreadsheets.readonly"]
)

sheets_service = build("sheets", "v4", credentials=creds)

# === LEER LINKS GUARDADOS ===
with open("menu_url.txt") as f:
    menu_url = f.read().strip()

with open("sheet_url.txt") as f:
    sheet_url_final = f.read().strip()

# === ACTUALIZAR LINKS EN LA PLANILLA ===
def actualizar_links_cliente(external_reference, sheet_url, menu_url):
    result = sheets_service.spreadsheets().values().get(
        spreadsheetId=CLIENTS_SHEET_ID,
        range=SHEET_NAME
    ).execute()
    rows = result.get("values", [])

    for idx, row in enumerate(rows):
        if len(row) > 11 and row[11] == external_reference:
            row_number = idx + 1  # porque es 1-based
            sheets_service.spreadsheets().values().batchUpdate(
                spreadsheetId=CLIENTS_SHEET_ID,
                body={
                    "valueInputOption": "RAW",
                    "data": [
                        {"range": f"{SHEET_NAME}!M{row_number}", "values": [[sheet_url]]},
                        {"range": f"{SHEET_NAME}!N{row_number}", "values": [[menu_url]]}
                    ]
                }
            ).execute()
            print(f"✅ Links actualizados en fila {row_number}")
            return
    print("⚠ External reference no encontrado")

# === LLAMAR A LA FUNCIÓN ===
external_reference = os.environ.get("EXTERNAL_REF")
if not external_reference:
    print("⚠ No se encontró EXTERNAL_REF en las variables de entorno")
else:
    actualizar_links_cliente(external_reference, sheet_url_final, menu_url)
