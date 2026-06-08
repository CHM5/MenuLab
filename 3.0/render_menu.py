import csv
from dataclasses import dataclass
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_IMG = "imagenbase.jpg"
CSV_PATH = "pirata.csv"          # tu CSV Plan 1
OUT_IMG = "render_out.jpg"

PIRATA_TTF = Path("fonts") / "PirataOne-Regular.ttf"
MARXIANA_REG_TTF = Path("fonts") / "TT Marxiana Trial Antiqua.ttf"
MARXIANA_ITALIC_TTF = Path("fonts") / "TT Marxiana Trial Antiqua Italic.ttf"

@dataclass
class Style:
    font: ImageFont.ImageFont
    fill: tuple[int, int, int]
    line_height_mult: float

def die(msg: str):
    raise SystemExit(f"[ERROR] {msg}")

def require_file(p: Path, label: str):
    if not p.exists():
        die(f"No encuentro {label}: '{p.resolve()}'")

def load_font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    require_file(path, f"fuente ({path.name})")
    return ImageFont.truetype(str(path), size=size)

def text_bbox(draw: ImageDraw.ImageDraw, s: str, font: ImageFont.ImageFont):
    return draw.textbbox((0, 0), s if s else "Ag", font=font)

def text_w(draw: ImageDraw.ImageDraw, s: str, font: ImageFont.ImageFont) -> int:
    b = text_bbox(draw, s, font)
    return b[2] - b[0]

def text_h(draw: ImageDraw.ImageDraw, s: str, font: ImageFont.ImageFont) -> int:
    b = text_bbox(draw, s, font)
    return b[3] - b[1]

def wrap_words(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int):
    out: list[str] = []
    for para in (text or "").splitlines():
        words = para.split()
        if not words:
            out.append("")
            continue
        line = words[0]
        for w in words[1:]:
            trial = f"{line} {w}"
            if text_w(draw, trial, font) <= max_width:
                line = trial
            else:
                out.append(line)
                line = w
        out.append(line)
    return out

def resolve_style(row: dict) -> Style:
    tipo = (row.get("TipoDato") or "").strip().lower()
    font_name = (row.get("Font") or "").strip().lower()
    size_raw = (row.get("Size") or "").strip()
    lhm_raw = (row.get("LineHeightMult") or "").strip()
    line_height_mult = float(lhm_raw) if lhm_raw else 1.4

    if tipo == "branding":
        return Style(font=load_font(PIRATA_TTF, 12), fill=(0, 0, 0), line_height_mult=line_height_mult)

    if size_raw == "":
        die(f"Fila sin Size: {row}")
    size = int(float(size_raw))

    if font_name == "pirata":
        f = load_font(PIRATA_TTF, size)
    elif font_name == "marxiana":
        f = load_font(MARXIANA_REG_TTF, size)
    elif font_name == "marxiana_italic":
        f = load_font(MARXIANA_ITALIC_TTF, size)
    else:
        die(f"Font inválida '{font_name}'. Usá: pirata|marxiana|marxiana_italic. Fila: {row}")

    return Style(font=f, fill=(0, 0, 0), line_height_mult=line_height_mult)

def draw_branding(draw: ImageDraw.ImageDraw, x: int, y: int, fill=(0, 0, 0)):
    f1 = load_font(PIRATA_TTF, 12)
    f2 = load_font(PIRATA_TTF, 15)
    line1 = "- Parrilla -"
    line2 = "EL PIRATA"
    draw.text((x, y), line1, font=f1, fill=fill)
    y2 = y + int(text_h(draw, line1, f1) * 1.4)
    draw.text((x, y2), line2, font=f2, fill=fill)

def draw_lines_in_box(draw, x, y, w, lines, font, fill, line_height_mult, align):
    cur_y = y
    for line in lines:
        line_w = text_w(draw, line, font)
        if align == "left":
            px = x
        elif align == "center":
            px = x + (w - line_w) // 2
        elif align == "right":
            px = x + (w - line_w)
        else:
            die(f"Align inválido: '{align}' (left|center|right)")
        draw.text((px, cur_y), line, font=font, fill=fill)
        cur_y += int(text_h(draw, line, font) * line_height_mult)

def main():
    require_file(Path(BASE_IMG), "imagen base")
    require_file(Path(CSV_PATH), "CSV")

    img = Image.open(BASE_IMG).convert("RGBA")
    draw = ImageDraw.Draw(img)

    with open(CSV_PATH, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)

        required = {"Item", "TipoDato", "X_px", "Y_px", "W_px", "Align", "Font", "Size", "LineHeightMult"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            die(f"Faltan columnas: {sorted(missing)}")

        has_text = "Text" in (reader.fieldnames or [])

        for row in reader:
            item = (row.get("Item") or "").strip()
            if not item:
                continue

            tipo = (row.get("TipoDato") or "").strip().lower()

            x = int(float(row["X_px"]))
            y = int(float(row["Y_px"]))
            w = int(float(row["W_px"]))
            align = (row.get("Align") or "left").strip().lower()

            if tipo == "branding":
                draw_branding(draw, x, y)
                continue

            style = resolve_style(row)

            # Si existe columna Text y tiene contenido, se usa tal cual (con \n).
            # Si no, usamos Item y wrap automático.
            raw_text = ""
            if has_text:
                raw_text = (row.get("Text") or "").strip()

            if raw_text:
                lines = raw_text.splitlines()
            else:
                lines = wrap_words(draw, item, style.font, w)

            draw_lines_in_box(
                draw, x, y, w, lines,
                font=style.font, fill=style.fill,
                line_height_mult=style.line_height_mult,
                align=align
            )

    img.convert("RGB").save(OUT_IMG, quality=95)
    print(f"[OK] Generado: {OUT_IMG}")

if __name__ == "__main__":
    main()