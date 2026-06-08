import cv2

img = cv2.imread("EL PIRATA.jpg")  # o "pir.jpg"
if img is None:
    raise FileNotFoundError("No se pudo abrir la imagen. Revisá nombre/ruta.")

print(img.shape)  # (height, width, channels)

