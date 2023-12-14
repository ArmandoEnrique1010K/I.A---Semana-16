import cv2
import numpy as np
from sklearn.cluster import KMeans


def contar_fichas_por_grupo(imagen, threshold=1, area_min=5, area_max=1000):
    imagen_copia = imagen.copy()

    # Aplicar técnicas de segmentación, umbralización, etc., para aislar las fichas
    # (aquí se asume que ya se ha aplicado el color)
    # ...
    # Supongamos que tienes un rango de color específico para las fichas (en formato HSV)
    # COLOR BLANCO
    lower_color = np.array([0, 0, 200])
    upper_color = np.array([180, 20, 255])
    mascara_color = cv2.inRange(imagen_copia, lower_color, upper_color)
    # UMBRALIZACIÓN
    imagen_procesada = cv2.bitwise_and(imagen_copia, imagen_copia, mask=mascara_color)
    gray = cv2.cvtColor(imagen_copia, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    imagen_procesada = cv2.bitwise_and(imagen_copia, imagen_copia, mask=thresh)
    # SEGMENTACIÓN
    # imagen_procesada = algoritmo_segmentacion(imagen_copia)

    # Encontrar contornos de las fichas
    hsv = cv2.cvtColor(imagen_copia, cv2.COLOR_BGR2HSV)
    _, thresh = cv2.threshold(hsv[:, :, 2], threshold, 255, cv2.THRESH_BINARY)
    contornos, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filtrar contornos por área
    contornos_filtrados = [
        cnt for cnt in contornos if area_min < cv2.contourArea(cnt) < area_max
    ]

    # Obtener los centros y radios de las fichas
    datos_fichas = np.array(
        [cv2.minEnclosingCircle(cnt) for cnt in contornos_filtrados]
    )

    # Asegúrate de que datos_fichas no está vacío
    if len(datos_fichas) > 0:
        # Tomar solo las coordenadas (x, y) y darle la forma adecuada
        centroides = np.array([dato[0] for dato in datos_fichas]).reshape(-1, 2)
        print(f"Shape de centroides: {centroides.shape}")

        # Utilizar KMeans para agrupar fichas
        kmeans = KMeans(n_clusters=2, random_state=0).fit(centroides)
        etiquetas_grupo = kmeans.labels_

        # Conteo por grupo
        num_fichas_grupo_1 = np.sum(etiquetas_grupo == 0)
        num_fichas_grupo_2 = np.sum(etiquetas_grupo == 1)

        return num_fichas_grupo_1, num_fichas_grupo_2
    else:
        print("No se encontraron fichas en la imagen.")
        return 0, 0
