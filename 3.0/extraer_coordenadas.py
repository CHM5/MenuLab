import pytesseract
from pytesseract import Output
from PIL import Image
import pandas as pd

# ---------------- CONFIGURACIÓN ----------------
# IMPORTANTE: Si estás en Windows, descomenta la línea de abajo y ajusta la ruta
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def generar_tabla_coordenadas(imagen_path, salida_excel):
    try:
        # 1. Cargar la imagen con PIL
        img = Image.open(imagen_path)
        
        # 2. Extraer datos con Tesseract (texto y coordenadas)
        # image_to_data devuelve un diccionario con info detallada de cada palabra
        datos = pytesseract.image_to_data(img, output_type=Output.DICT, lang='spa') # 'spa' para español si está instalado, sino 'eng'
        
        filas = []
        n_cajas = len(datos['text'])
        
        # 3. Iterar sobre cada elemento detectado
        for i in range(n_cajas):
            # Obtener el texto detectado
            texto = datos['text'][i].strip()
            confianza = int(datos['conf'][i])
            
            # Filtramos espacios vacíos y lecturas de muy baja confianza
            if texto != "" and confianza > 40:
                
                # Intentar adivinar el "Tipo de dato" (Lógica básica)
                # Esto es difícil de automatizar 100% sin IA, pero podemos dejarlo en blanco
                # o categorizar como "Posible Título" si es muy grande (altura de caja).
                tipo_dato = "" 
                
                nueva_fila = {
                    'Tipo de dato': tipo_dato,           # Columna para completar (categoria/plato/etc)
                    'Item': texto,                       # El texto encontrado (ej: Parrilla, Papas, etc)
                    'Eje x': datos['left'][i],           # Coordenada izquierda
                    'Eje y': datos['top'][i],            # Coordenada superior
                    'Tamaño de letra': '',               # En blanco para completar manualmente
                    'Fuente de letra': '',               # En blanco para completar manualmente
                    'Interlineado': '',                  # En blanco para completar manualmente
                    'Interletrado': ''                   # En blanco para completar manualmente
                }
                filas.append(nueva_fila)

        # 4. Crear DataFrame y Exportar
        df = pd.DataFrame(filas)
        
        # Asegurar el orden de columnas que pediste
        columnas_ordenadas = [
            'Tipo de dato', 'Item', 'Eje x', 'Eje y', 
            'Tamaño de letra', 'Fuente de letra', 'Interlineado', 'Interletrado'
        ]
        
        # Si alguna columna no existe (porque no se llenó), pandas la crea vacía, 
        # pero forzamos el reindex para asegurar que estén todas.
        df = df.reindex(columns=columnas_ordenadas)
        
        # Guardar a Excel
        df.to_excel(salida_excel, index=False)
        print(f"¡Éxito! Archivo guardado como: {salida_excel}")
        print(f"Se encontraron {len(df)} elementos de texto.")

    except Exception as e:
        print(f"Ocurrió un error: {e}")
        print("¿Tienes instalado Tesseract OCR y la ruta configurada?")

# Ejecutar la función
# Asegúrate de que la imagen 'objetolimpio.jpg' esté en la misma carpeta
if __name__ == "__main__":
    generar_tabla_coordenadas("objetivo_limpio.jpg", "tabla_menu.xlsx")