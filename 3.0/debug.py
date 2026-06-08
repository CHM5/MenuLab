import csv
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_IMG = "imagenbase.jpg"
CSV_PATH = "Menulab3.0 - pirata.csv"
OUT_IMG = "render_out.jpg"

FONT_TITLE_TTF = Path("fonts") / "PirataOne-Regular.ttf"

def font(ttf_path: Path, size: int):
    if ttf_path.exists():
        return ImageFont.truetype(str(ttf_path), size=size)
    return ImageFont.load_default()

def get_style(tipo: str):
    """
    Ajustes iniciales (aproximados).
    Después los calibramos mirando el resultado vs objetivo.jpg.
    """
    tipo = (tipo or "").lower().strip()

    if tipo == "branding":
        return dict(font=font(FONT_TITLE_TTF, 44), fill=(0, 0, 0), stroke_width=0, stroke_fill=None)
    if tipo == "categoria":
        return dict(font=font(FONT_TITLE_TTF, 42), fill=(0, 0, 0), stroke_width=0, stroke_fill=None)
    if tipo == "plato":
        return dict(font=font(FONT_TITLE_TTF, 30), fill=(0, 0, 0), stroke_width=0, stroke_fill=None)
    if tipo in ("descripcion", "nota"):
        # para debug final: usamos PirataOne también; si querés más fidelidad quizá convenga otra serif/italic
        return dict(font=font(FONT_TITLE_TTF, 22), fill=(0, 0, 0), stroke_width=0, stroke_fill=None)
    if tipo == "extra":
        return dict(font=font(FONT_TITLE_TTF, 28), fill=(0, 0, 0), stroke_width=0, stroke_fill=None)

    return dict(font=font(FONT_TITLE_TTF, 24), fill=(0, 0, 0), stroke_width=0, stroke_fill=None)

def main():
    img = Image.open(BASE_IMG).convert("RGBA")
    draw = ImageDraw.Draw(img)

    with open(CSV_PATH, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            item = (row.get("Item") or "").strip()
            tipo = (row.get("TipoDato") or "").strip()

            if not item:
                continue

            x = int(float(row["X_px"]))
            y = int(float(row["Y_px"]))

            style = get_style(tipo)
            draw.text(
                (x, y),
                item,
                font=style["font"],
                fill=style["fill"],
                stroke_width=style["stroke_width"],
                stroke_fill=style["stroke_fill"],
            )

    img.convert("RGB").save(OUT_IMG, quality=95)
    print(f"OK -> {OUT_IMG}")

if __name__ == "__main__":
    main()