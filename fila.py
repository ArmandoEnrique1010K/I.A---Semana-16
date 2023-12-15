import cv2
import numpy as np


class ContadorFilas:
    def __init__(self, area_minima, area_maxima):
        # Variables de control
        self.color_rango = None
        self.resultado_label_text = None
        self.area_minima = area_minima
        self.area_maxima = area_maxima

    def contar_fichas_por_filas(self, imagen_path, color_rango):
        # Lógica para contar fichas por filas
        imagen = cv2.imread(imagen_path)
        imagen_hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

        # Obtener el rango de color especificado por el usuario
        color_min = np.array(color_rango[:3], np.uint8)
        color_max = np.array(color_rango[3:], np.uint8)

        # Crear la máscara
        mask_color = cv2.inRange(imagen_hsv, color_min, color_max)

        # Encontrar contornos en la imagen
        contours, _ = cv2.findContours(
            mask_color, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        # Filtrar contornos por área
        area_minima = int(self.area_minima.get())
        area_maxima = int(self.area_maxima.get())
        fichas_por_fila = 0

        for contour in contours:
            area = cv2.contourArea(contour)
            if area_minima < area < area_maxima:
                fichas_por_fila += 1

        # Dibujar contornos en la imagen
        cv2.drawContours(imagen, contours, -1, (0, 255, 0), 2)

        max_width = 800
        max_height = 600
        imagen = self.redimensionar_imagen(imagen, max_width, max_height)

        # Visualizar imagen con contornos
        cv2.imshow("Contours", imagen)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return fichas_por_fila

    def redimensionar_imagen(self, imagen, max_width, max_height):
        # Obtener dimensiones originales
        height, width, _ = imagen.shape

        # Calcular nuevos tamaños manteniendo la proporción original
        ratio = min(max_width / width, max_height / height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)

        # Redimensionar la imagen
        imagen_redimensionada = cv2.resize(imagen, (new_width, new_height))

        return imagen_redimensionada
