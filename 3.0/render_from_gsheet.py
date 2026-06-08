import csv
import io
import os
import time
import requests
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

BACKGROUND_PATH = "EL PIRATA.jpg"
OUTPUT_PATH = f"EL_PIRATA_homography_{time.strftime('%Y%m%d_%H%M%S')}.png"

PUBLISHED_CSV_URL = (
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vReWs-XMsP7-mnsbBw0QsyLbUL8LF2IiVq8wO_5ECWoa055ML0OZ9t0UZV92yYuM9TdEmbkSDfHxOSt/pub"
    "?gid=926989482&single=true&output=csv"
)

# Fonts
PIRATA_ONE_TTF = "fonts/PirataOne-Regular.ttf"
TT_MARXIANA_REG = "fonts/TTMarxianaAntiqua-Regular.ttf"
TT_MARXIANA_ITALIC = "fonts/TTMarxianaAntiqua-Italic.ttf"

FALLBACK_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
FALLBACK_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FALLBACK_ITALIC = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf"

ANCHOR_MODE = "top"
LEADING = 1.15

STYLE = {
    "branding": {"kind": "title", "size": 26, "fill": (20, 10, 10)},
    "categoria": {"kind": "title", "size": 36, "fill": (20, 10, 10)},
    "plato": {"kind": "body_bold", "size": 22, "fill": (20, 10, 10)},
    "descripcion": {"kind": "body_italic", "size": 16, "fill": (35, 20, 20)},
    "nota": {"kind": "body_italic", "size": 15, "fill": (35, 20, 20)},
    "extra": {"kind": "body_bold", "size": 22, "fill": (20, 10, 10)},
}
DEFAULT_STYLE = {"kind": "body_reg", "size": 16, "fill": (0, 0, 0)}

# Tus puntos: (old from CSV) -> (new correct in pir.jpg / target)
CAL_POINTS = [
    ("HAMBURGUESAS", (760, 186), (918, 267)),
    ("SANDWICHES", (484, 248), (522, 364)),
    ("GUARNICIONES", (129, 815), (173, 1294)),
    ("EXTRAS", (891, 763), (1080, 1234)),
    ("MILANESAS AL PLATO", (498, 683), (553, 1104)),
]

# Debug: dibuja los puntos calibrados
DRAW_CAL_POINTS = True


def download_csv_no_cache(url: str) -> str:
    sep = "&" if "?" in url else "?"
    url2 = f"{url}{sep}t={int(time.time())}"
    r = requests.get(url2, timeout=30, headers={"Cache-Control": "no-cache"})
    r.raise_for_status()
    r.encoding = "utf-8"
    return r.text


def coerce_number(v: str) -> float:
    return float(str(v).strip().replace(",", "."))


def font_path_for(kind: str) -> str:
    if kind == "title":
        if not os.path.exists(PIRATA_ONE_TTF):
            raise FileNotFoundError(f"Falta {PIRATA_ONE_TTF}")
        return PIRATA_ONE_TTF

    if kind == "body_reg":
        return TT_MARXIANA_REG if os.path.exists(TT_MARXIANA_REG) else FALLBACK_REG

    if kind == "body_bold":
        return FALLBACK_BOLD if not os.path.exists(TT_MARXIANA_REG) else TT_MARXIANA_REG

    if kind == "body_italic":
        if os.path.exists(TT_MARXIANA_ITALIC):
            return TT_MARXIANA_ITALIC
        return FALLBACK_ITALIC

    return FALLBACK_REG


def get_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size=size)


def draw_text_anchor(draw, x, y, text, font, fill, anchor_mode: str):
    if anchor_mode == "top":
        draw.text((x, y), text, font=font, fill=fill)
        return
    if anchor_mode == "baseline":
        ascent, descent = font.getmetrics()
        draw.text((x, y - ascent), text, font=font, fill=fill)
        return
    raise ValueError("ANCHOR_MODE debe ser 'top' o 'baseline'")


def solve_homography(points):
    src = np.array([p[1] for p in points], dtype=np.float32)  # old
    dst = np.array([p[2] for p in points], dtype=np.float32)  # new
    # RANSAC por robustez (por si 1 punto tiene error humano)
    H, mask = cv2.findHomography(src, dst, method=cv2.RANSAC, ransacReprojThreshold=3.0)
    if H is None:
        raise RuntimeError("No se pudo calcular homografía (H=None).")
    return H, mask


def apply_homography(x, y, H):
    pt = np.array([[[float(x), float(y)]]], dtype=np.float32)  # shape (1,1,2)
    out = cv2.perspectiveTransform(pt, H)[0][0]
    return int(round(out[0])), int(round(out[1]))


def draw_cross(draw: ImageDraw.ImageDraw, x: int, y: int, color=(255, 0, 0, 200), s=10):
    draw.line((x - s, y, x + s, y), fill=color, width=3)
    draw.line((x, y - s, x, y + s), fill=color, width=3)


def main():
    H, mask = solve_homography(CAL_POINTS)
    print("[H] homography matrix:\n", H)
    print("[H] inliers mask:", mask.ravel().tolist())

    # Check cal points error
    for name, (xo, yo), (xt, yt) in CAL_POINTS:
        xr, yr = apply_homography(xo, yo, H)
        print(f"[check] {name:18s} target=({xt},{yt}) got=({xr},{yr}) err=({xr-xt},{yr-yt})")

    img = Image.open(BACKGROUND_PATH).convert("RGBA")
    draw = ImageDraw.Draw(img)

    # dibujar puntos target para ver rápido si calza
    if DRAW_CAL_POINTS:
        for name, _, (xt, yt) in CAL_POINTS:
            draw_cross(draw, xt, yt, color=(0, 255, 0, 200), s=12)
            draw.text((xt + 14, yt - 10), name, fill=(0, 255, 0, 200))

    csv_text = download_csv_no_cache(PUBLISHED_CSV_URL)
    reader = csv.DictReader(io.StringIO(csv_text))

    rendered = 0
    for row in reader:
        item = (row.get("Item") or "").replace("\\n", "\n").strip()
        tipo = (row.get("TipoDato") or "").strip().lower()
        if not item:
            continue

        x_old = coerce_number(row["X_px"])
        y_old = coerce_number(row["Y_px"])
        x, y = apply_homography(x_old, y_old, H)

        st = STYLE.get(tipo, DEFAULT_STYLE)
        fpath = font_path_for(st["kind"])
        font = get_font(fpath, st["size"])

        lines = item.split("\n")
        ascent, descent = font.getmetrics()
        line_h = int((ascent + descent) * LEADING)

        for i, line in enumerate(lines):
            yy = y + i * line_h
            draw_text_anchor(draw, x, yy, line, font, st["fill"], ANCHOR_MODE)

        rendered += 1

    img.save(OUTPUT_PATH)
    print("[ok] Rendered:", rendered, "->", OUTPUT_PATH)


if __name__ == "__main__":
    main()