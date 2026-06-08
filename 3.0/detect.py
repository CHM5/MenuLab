import csv
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np

IMG_IN = "objetivo_limpio.jpg"   # <-- poné acá el nombre real de la imagen limpia
OUT_CSV = "detected_boxes.csv"

@dataclass
class Box:
    x: int
    y: int
    w: int
    h: int
    area: int

def main():
    img = cv2.imread(IMG_IN)
    if img is None:
        raise SystemExit(f"No pude leer {IMG_IN}")

    h, w = img.shape[:2]
    print(f"[INFO] image size: {w}x{h}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # binarización: texto negro -> blanco
    # Otsu suele andar muy bien en fondo blanco
    _, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Conectar letras en palabras/lineas (ajustable)
    # kernel horizontal para unir caracteres en una misma línea
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 3))
    joined = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel, iterations=1)

    # Encontrar contornos (cajas de líneas o palabras)
    contours, _ = cv2.findContours(joined, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    boxes: list[Box] = []
    for c in contours:
        x, y, ww, hh = cv2.boundingRect(c)
        area = ww * hh

        # Filtros para ignorar ruido (ajustables)
        if area < 150:      # muy chico
            continue
        if hh < 8:          # muy bajo (puntos/ruido)
            continue
        if ww < 20:         # muy angosto
            continue

        boxes.append(Box(x=x, y=y, w=ww, h=hh, area=area))

    # Orden visual: de arriba hacia abajo, luego izquierda a derecha
    boxes.sort(key=lambda b: (b.y, b.x))

    with open(OUT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["x", "y", "w", "h", "x2", "y2", "area"])
        writer.writeheader()
        for b in boxes:
            writer.writerow({
                "x": b.x,
                "y": b.y,
                "w": b.w,
                "h": b.h,
                "x2": b.x + b.w,
                "y2": b.y + b.h,
                "area": b.area,
            })

    print(f"[OK] wrote {OUT_CSV} with {len(boxes)} boxes")

    # Debug: imagen con rectángulos
    debug = img.copy()
    for b in boxes:
        cv2.rectangle(debug, (b.x, b.y), (b.x + b.w, b.y + b.h), (0, 0, 255), 1)
    cv2.imwrite("detected_boxes_debug.jpg", debug)
    print("[OK] wrote detected_boxes_debug.jpg")

if __name__ == "__main__":
    main()