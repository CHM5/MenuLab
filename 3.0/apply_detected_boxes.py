import csv
from collections import defaultdict

MENU_IN = "Menulab3.0 - pirata.csv"   # tu menú original (4 columnas)
BOXES_IN = "detected_boxes.csv"      # cajas detectadas
OUT = "pirata.autobox.csv"           # salida Plan 1

# Umbrales de columna (ajustables según tu imagen limpia)
# Basado en tu detected_boxes.csv: hay cajas con x~159, ~480-552, ~913+
def box_column(x: int) -> str:
    if x < 380:
        return "L"
    if x < 820:
        return "C"
    return "R"

def menu_column(x: int) -> str:
    # tus X originales: izquierda ~117, centro ~392-508, derecha ~685-891
    if x < 300:
        return "L"
    if x < 650:
        return "C"
    return "R"

def style_defaults(tipo: str):
    tipo = (tipo or "").strip().lower()
    if tipo == "categoria":
        return "left", "pirata", 20, 1.55
    if tipo == "branding":
        return "left", "pirata", 0, 1.4
    if tipo == "plato":
        return "left", "marxiana", 13, 1.4
    if tipo in ("descripcion", "nota"):
        return "left", "marxiana_italic", 13, 1.4
    if tipo == "extra":
        return "left", "marxiana", 13, 1.4
    return "left", "marxiana", 13, 1.4

def load_boxes():
    boxes_by_col = defaultdict(list)
    with open(BOXES_IN, "r", encoding="utf-8-sig", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            x = int(float(row["x"]))
            y = int(float(row["y"]))
            w = int(float(row["w"]))
            h = int(float(row["h"]))
            col = box_column(x)
            boxes_by_col[col].append({"x": x, "y": y, "w": w, "h": h})

    # ordenar por y dentro de cada columna
    for col in boxes_by_col:
        boxes_by_col[col].sort(key=lambda b: (b["y"], b["x"]))

    return boxes_by_col

def load_menu():
    items_by_col = defaultdict(list)
    with open(MENU_IN, "r", encoding="utf-8-sig", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            item = (row.get("Item") or "").strip()
            tipo = (row.get("TipoDato") or "").strip()
            if not item:
                continue

            x = int(float(row["X_px"]))
            y = int(float(row["Y_px"]))
            col = menu_column(x)

            items_by_col[col].append({
                "Item": item,
                "TipoDato": tipo,
                "X_px": x,
                "Y_px": y,
            })

    # importante: mantener orden visual original dentro de cada columna (por y)
    for col in items_by_col:
        items_by_col[col].sort(key=lambda r: (r["Y_px"], r["X_px"]))

    return items_by_col

def main():
    boxes = load_boxes()
    menu = load_menu()

    # chequeo rápido de conteos por columna
    for col in ("L", "C", "R"):
        print(f"[INFO] col {col}: menu_items={len(menu[col])} boxes={len(boxes[col])}")

    out_rows = []

    for col in ("L", "C", "R"):
        mi = menu[col]
        bi = boxes[col]

        if len(bi) < len(mi):
            raise SystemExit(
                f"ERROR: En columna {col} hay menos cajas detectadas ({len(bi)}) "
                f"que items de menú ({len(mi)}). Hay que ajustar detección/filtros."
            )

        # asignación 1 a 1 por orden
        for idx, m in enumerate(mi):
            b = bi[idx]
            align, font, size, lhm = style_defaults(m["TipoDato"])

            out_rows.append({
                "Item": m["Item"],
                "TipoDato": m["TipoDato"],
                "X_px": m["X_px"],         # mantenemos tu X/Y original
                "Y_px": m["Y_px"],
                "W_px": b["w"],            # tomamos W de la caja detectada
                "Align": align,
                "Font": font,
                "Size": size,
                "LineHeightMult": lhm,
                "BoxX": b["x"],            # debug
                "BoxY": b["y"],            # debug
            })

    # reordenar como el CSV original (por Y, luego X)
    out_rows.sort(key=lambda r: (r["Y_px"], r["X_px"]))

    with open(OUT, "w", encoding="utf-8", newline="") as f:
        fieldnames = ["Item","TipoDato","X_px","Y_px","W_px","Align","Font","Size","LineHeightMult","BoxX","BoxY"]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(out_rows)

    print(f"[OK] wrote {OUT}")

if __name__ == "__main__":
    main()