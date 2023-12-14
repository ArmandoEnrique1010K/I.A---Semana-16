import cv2
import numpy as np


def contar_fichas_por_color(
    imagen,
    rango_color,
    threshold=0.6,
    area_min=5,
    area_max=1000,
    color_contornos=(0, 255, 0),
):
    # Crear una copia de la imagen para evitar modificar la original
    imagen_copia = imagen.copy()

    try:
        hsv = cv2.cvtColor(imagen_copia, cv2.COLOR_BGR2HSV)
    except cv2.error:
        raise ValueError(
            "La imagen proporcionada no es válida. Asegúrate de que sea una imagen en color."
        )

    lower_color = np.array(rango_color[0])
    upper_color = np.array(rango_color[1])
    mascara = cv2.inRange(hsv, lower_color, upper_color)
    fichas_color = cv2.bitwise_and(imagen_copia, imagen_copia, mask=mascara)
    gray = cv2.cvtColor(fichas_color, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    contornos, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    num_fichas = len(contornos)

    # Filtrar contornos por área
    contornos_filtrados = [
        cnt for cnt in contornos if area_min < cv2.contourArea(cnt) < area_max
    ]

    # Dibujar contornos en la imagen con fichas coloreadas
    cv2.drawContours(fichas_color, contornos_filtrados, -1, color_contornos, 2)

    num_fichas = len(contornos_filtrados)
    return fichas_color, num_fichas
