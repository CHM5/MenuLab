import csv
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_IMG = "imagenbase.jpg"
CSV_PATH = "Menulab3.0 - pirata.csv"
OUT_IMG = "debug_overlay.jpg"

# Tipografías (debug)
FONT_TTF = Path("fonts") / "PirataOne-Regular.ttf"

def load_font(size: int):
    if FONT_TTF.exists():
        return ImageFont.truetype(str(FONT_TTF), size=size)
    return ImageFont.load_default()

def draw_cross(draw: ImageDraw.ImageDraw, x: int, y: int, size: int = 6, color=(255, 0, 0)):
    draw.line((x - size, y, x + size, y), fill=color, width=2)
    draw.line((x, y - size, x, y + size), fill=color, width=2)

def main():
    img = Image.open(BASE_IMG).convert("RGBA")
    draw = ImageDraw.Draw(img)

    font = load_font(18)

    with open(CSV_PATH, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=1):
            item = (row.get("Item") or "").strip()
            tipo = (row.get("TipoDato") or "").strip()
            try:
                x = int(float(row.get("X_px")))
                y = int(float(row.get("Y_px")))
            except Exception:
                print(f"[WARN] Línea {i}: coordenadas inválidas: {row}")
                continue

            # Cruz en el punto top-left
            draw_cross(draw, x, y, size=7, color=(255, 0, 0))

            # Label
            label = f"{tipo}: {item}"
            # fondo semi-transparente para leerlo
            pad = 3
            bbox = draw.textbbox((x + 10, y - 2), label, font=font)
            bx0, by0, bx1, by1 = bbox
            draw.rectangle((bx0 - pad, by0 - pad, bx1 + pad, by1 + pad), fill=(255, 255, 255, 180))
            draw.text((x + 10, y - 2), label, fill=(0, 0, 0, 255), font=font)

    img.convert("RGB").save(OUT_IMG, quality=95)
    print(f"OK -> {OUT_IMG}")

if __name__ == "__main__":
    main()