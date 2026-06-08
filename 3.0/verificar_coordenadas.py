from PIL import Image, ImageDraw, ImageFont
import os

# 1. TUS IMÁGENES (Asegurate que existan en la carpeta)
# Ajusta los nombres de archivo si los guardaste diferente
IMG_HOJA_1 = "hoja1.jpg"  # La imagen de Entradas/Sándwichs
IMG_HOJA_2 = "hoja2.jpg"  # La imagen de Hamburguesas/Parrilla

# 2. LOS DATOS DE LA BASE DE DATOS (Simulación del SQL)
# Formato: (Página, Nombre, X, Y)
# X e Y son porcentajes (0.0 a 1.0)
datos_db = [
    # ==========================================
    # HOJA 1: ENTRADAS & SANDWICHS (Panel Izquierdo del Tríptico)
    # X ajustado a ~0.21 (Zona de precios del primer panel)
    # ==========================================
    {"page": 1, "name": "Empanadas", "x": 0.21, "y": 0.235},
    {"page": 1, "name": "Lengua", "x": 0.21, "y": 0.305},
    {"page": 1, "name": "Berenjenas", "x": 0.21, "y": 0.340},
    
    {"page": 1, "name": "Lomo", "x": 0.21, "y": 0.605},
    {"page": 1, "name": "Bondiola", "x": 0.21, "y": 0.640},
    {"page": 1, "name": "Milanesa", "x": 0.21, "y": 0.680},
    {"page": 1, "name": "Ojo de bife", "x": 0.21, "y": 0.720},
    {"page": 1, "name": "Super pancho", "x": 0.21, "y": 0.760},

    # ==========================================
    # HOJA 2: INTERIOR (3 Paneles)
    # ==========================================
    
    # --- COLUMNA 1: HAMBURGUESAS (X ~ 0.27) ---
    {"page": 2, "name": "Explosiva", "x": 0.27, "y": 0.105},
    {"page": 2, "name": "La Doble", "x": 0.27, "y": 0.200},
    {"page": 2, "name": "Simple", "x": 0.27, "y": 0.260},
    {"page": 2, "name": "Veggie", "x": 0.27, "y": 0.290},
    
    # Adicionales
    {"page": 2, "name": "Jamon", "x": 0.27, "y": 0.495},
    {"page": 2, "name": "Queso", "x": 0.27, "y": 0.520},
    {"page": 2, "name": "Cebolla", "x": 0.27, "y": 0.545},
    {"page": 2, "name": "Panceta", "x": 0.27, "y": 0.570},
    {"page": 2, "name": "Huevo", "x": 0.27, "y": 0.595},
    
    # Cervezas
    {"page": 2, "name": "Stella", "x": 0.27, "y": 0.740},
    {"page": 2, "name": "Stella N", "x": 0.27, "y": 0.770},
    {"page": 2, "name": "Heineken", "x": 0.27, "y": 0.795},
    {"page": 2, "name": "Corona", "x": 0.27, "y": 0.845},
    {"page": 2, "name": "Patagonia", "x": 0.27, "y": 0.870},
    {"page": 2, "name": "Pat. Hoppy", "x": 0.27, "y": 0.895},
    {"page": 2, "name": "Pat. Amber", "x": 0.27, "y": 0.920},

    # --- COLUMNA 2: PARRILLA (X ~ 0.61) ---
    # Nota: Parrillada tiene el precio abajo del texto, ajusté Y
    {"page": 2, "name": "Parrillada x3", "x": 0.52, "y": 0.220}, 
    {"page": 2, "name": "Pollo Entero", "x": 0.63, "y": 0.270},
    {"page": 2, "name": "1/4 Pollo", "x": 0.63, "y": 0.300},
    {"page": 2, "name": "Ojo de bife", "x": 0.63, "y": 0.330},
    {"page": 2, "name": "1/2 Ojo", "x": 0.63, "y": 0.360},
    {"page": 2, "name": "Chori Simple", "x": 0.63, "y": 0.420},
    {"page": 2, "name": "Chori Comp", "x": 0.63, "y": 0.450},
    {"page": 2, "name": "Chori Cerdo", "x": 0.63, "y": 0.480},
    {"page": 2, "name": "Morcilla", "x": 0.63, "y": 0.515},

    # Bebidas (Columna central baja)
    {"page": 2, "name": "Pepsi", "x": 0.56, "y": 0.645},
    {"page": 2, "name": "7up", "x": 0.56, "y": 0.670},
    {"page": 2, "name": "Agua Sab.", "x": 0.56, "y": 0.815},
    {"page": 2, "name": "Agua", "x": 0.56, "y": 0.915},
    
    # --- COLUMNA 3: AL PLATO (X ~ 0.92) ---
    {"page": 2, "name": "Mila Caballo", "x": 0.92, "y": 0.095},
    {"page": 2, "name": "Mila Napo", "x": 0.92, "y": 0.125},
    {"page": 2, "name": "Mila Sola", "x": 0.92, "y": 0.155},
    
    # Guarniciones
    {"page": 2, "name": "Ensalada Mix", "x": 0.92, "y": 0.315},
    {"page": 2, "name": "Papas Fritas", "x": 0.92, "y": 0.405},
    
    # Vinos
    {"page": 2, "name": "Dante", "x": 0.92, "y": 0.640},
    {"page": 2, "name": "Elementos", "x": 0.92, "y": 0.670},
    {"page": 2, "name": "Finca Moras", "x": 0.92, "y": 0.700},
    {"page": 2, "name": "Trivento", "x": 0.92, "y": 0.850},
]   
def dibujar_items(ruta_imagen, numero_pagina, datos):
    if not os.path.exists(ruta_imagen):
        print(f"⚠️ Error: No encontré el archivo {ruta_imagen}")
        return

    # Abrir imagen
    img = Image.open(ruta_imagen)
    draw = ImageDraw.Draw(img)
    width, height = img.size
    
    # Intentar cargar una fuente, sino usar default
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()

    print(f"Procesando Página {numero_pagina}...")

    for item in datos:
        if item["page"] == numero_pagina:
            # CALCULO MATEMÁTICO:
            # Convertir porcentaje (0.5) a pixel real (0.5 * 1000px = 500px)
            pixel_x = item["x"] * width
            pixel_y = item["y"] * height
            
            # Dibujar punto rojo (donde iría el precio o el click)
            r = 10 # radio del punto
            draw.ellipse((pixel_x-r, pixel_y-r, pixel_x+r, pixel_y+r), fill="red", outline="white")
            
            # Dibujar texto de referencia
            draw.text((pixel_x + 15, pixel_y - 10), item["name"], fill="blue", font=font, stroke_width=2, stroke_fill="white")

    # Guardar resultado
    nombre_salida = f"prueba_hoja{numero_pagina}.jpg"
    img.save(nombre_salida)
    print(f"✅ Guardado: {nombre_salida}")

# Ejecutar
dibujar_items(IMG_HOJA_1, 1, datos_db)
dibujar_items(IMG_HOJA_2, 2, datos_db)