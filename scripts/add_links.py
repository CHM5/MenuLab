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
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)

sheets_service = build("sheets", "v4", credentials=creds)

# === LEER VARIABLES DE ENTORNO ===
external_ref = os.environ.get("EXTERNAL_REF")
menu_url = os.environ.get("MENU_URL")
sheet_url = os.environ.get("SHEET_URL")

if not (external_ref and menu_url and sheet_url):
    print("⚠ Faltan variables de entorno necesarias (EXTERNAL_REF, MENU_URL o SHEET_URL)")
    exit(1)

# === ACTUALIZAR CLIENTES SHEET ===
def update_client_sheet(external_reference, sheet_url, menu_url):
    result = sheets_service.spreadsheets().values().get(
        spreadsheetId=CLIENTS_SHEET_ID,
        range=SHEET_NAME
    ).execute()
    rows = result.get('values', [])

    for idx, row in enumerate(rows):
        if len(row) > 11 and row[11] == external_reference:
            row_number = idx + 1
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
    print(f"⚠ External reference {external_reference} no encontrado en Clientes")

# === EJECUTAR ===
update_client_sheet(external_ref, sheet_url, menu_url)
