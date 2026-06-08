import csv

IN_CSV = "Menulab3.0 - pirata.csv"   # tu CSV original (4 columnas)
OUT_CSV = "pirata.csv"              # CSV extendido (Plan 1)

def defaults(tipo: str, x: int):
    tipo = (tipo or "").strip().lower()

    # W_px por zona (defaults; luego ajustás finito)
    if x < 300:
        w = 320
    elif x < 650:
        w = 380
    elif x < 820:
        w = 260
    else:
        w = 260

    # Styles
    if tipo == "categoria":
        return w, "left", "pirata", 20, 1.55
    if tipo == "branding":
        # size 0 porque lo dibujamos especial (12/15) en render_menu_boxes.py
        return w, "left", "pirata", 0, 1.4
    if tipo == "plato":
        return w, "left", "marxiana", 13, 1.4
    if tipo in ("descripcion", "nota"):
        return w, "left", "marxiana_italic", 13, 1.4
    if tipo == "extra":
        return w, "left", "marxiana", 13, 1.4

    return w, "left", "marxiana", 13, 1.4

def main():
    with open(IN_CSV, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        required = {"Item", "TipoDato", "X_px", "Y_px"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"El CSV de entrada no tiene columnas requeridas: {sorted(missing)}")

        rows_out = []
        for row in reader:
            item = (row.get("Item") or "").strip()
            tipo = (row.get("TipoDato") or "").strip()
            if not item:
                continue

            x = int(float(row["X_px"]))
            y = int(float(row["Y_px"]))

            w, align, font, size, lhm = defaults(tipo, x)

            rows_out.append({
                "Item": item,
                "TipoDato": tipo,
                "X_px": x,
                "Y_px": y,
                "W_px": w,
                "Align": align,
                "Font": font,
                "Size": size,
                "LineHeightMult": lhm,
            })

    with open(OUT_CSV, "w", encoding="utf-8", newline="") as f:
        fieldnames = ["Item", "TipoDato", "X_px", "Y_px", "W_px", "Align", "Font", "Size", "LineHeightMult"]
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(rows_out)

    print(f"OK -> generado {OUT_CSV} (Plan 1) a partir de {IN_CSV}")

if __name__ == "__main__":
    main()