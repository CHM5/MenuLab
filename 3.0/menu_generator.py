import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os

def generar_menu_naranja(csv_path, imagen_base_path, output_path):
    print("--- Generando Menú en Naranja ---")
    
    if not os.path.exists(imagen_base_path):
        print("No encuentro la imagen base.")
        return

    # 1. Preparar imagen
    img = Image.open(imagen_base_path).convert("RGBA")
    txt_layer = Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)
    
    # 2. DEFINIR EL COLOR NARANJA
    # Opción A: Naranja "Pirata" (Más oscuro, tipo óxido/ladrillo). SE LEE MEJOR.
    color_texto = (160, 50, 0, 255) 
    
    # Opción B: Naranja "Vivo" (Más brillante, tipo fruta). Descomenta si prefieres este.
    # color_texto = (255, 120, 0, 255)

    # 3. Configuración de Escala (Ajusta si el texto sale muy grande o chico)
    ESCALA = 1.0 
    
    try:
        # Rutas a tus fuentes
        fuentes = {
            'branding':    ImageFont.truetype("fonts/PirataOne-Regular.ttf", int(50 * ESCALA)),
            'categoria':   ImageFont.truetype("fonts/PirataOne-Regular.ttf", int(40 * ESCALA)),
            'plato':       ImageFont.truetype("fonts/TT Marxiana Trial Antiqua.ttf", int(28 * ESCALA)),
            'extra':       ImageFont.truetype("fonts/TT Marxiana Trial Antiqua.ttf", int(26 * ESCALA)),
            'descripcion': ImageFont.truetype("fonts/TT Marxiana Trial Antiqua Italic.ttf", int(22 * ESCALA)),
            'nota':        ImageFont.truetype("fonts/TT Marxiana Trial Antiqua Italic.ttf", int(20 * ESCALA))
        }
    except Exception as e:
        print(f"Error cargando fuentes: {e}")
        return

    df = pd.read_csv(csv_path)

    for index, row in df.iterrows():
        try:
            texto = str(row['Item']).strip().replace('"', '')
            tipo = row['TipoDato']
            
            # Coordenadas
            x = int(row['X_px'])
            y = int(row['Y_px'])

            # Selección de fuente
            font = fuentes.get(tipo, fuentes['plato'])
            
            # DIBUJAR EN NARANJA
            draw.text((x, y), texto, font=font, fill=color_texto, anchor="la")

        except Exception:
            continue

    # Guardar
    salida = Image.alpha_composite(img, txt_layer).convert("RGB")
    salida.save(output_path, quality=95)
    print(f"✅ ¡Listo! Menú naranja guardado en: {output_path}")

if __name__ == "__main__":
    generar_menu_naranja('pirata.csv', 'objetivo_limpio.jpg', 'menu_naranja.jpg')