import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk


class ContadorGrupos:
    def __init__(self, area_minima, area_maxima):
        # Variables de control
        self.color_rango = None
        self.resultado_label_text = None
        self.area_minima = area_minima
        self.area_maxima = area_maxima

    def contar_fichas_por_grupos(self, imagen_path, color_rango):
        # Lógica para contar fichas por grupos
        imagen = cv2.imread(imagen_path)
        imagen_hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

        # Obtener el rango de color especificado por el usuario
        color_min = np.array(color_rango[:3], np.uint8)
        color_max = np.array(color_rango[3:], np.uint8)

        # Crear la máscara
        mask_color = cv2.inRange(imagen_hsv, color_min, color_max)

        # Aplicar un filtro de borde (ajusta los valores según tus necesidades)
        edges = cv2.Canny(mask_color, 30, 100)

        # Obtener el color del rango máximo para el borde
        border_color = tuple(color_max.tolist())

        # Binarización usando el color del borde
        _, binary_image = cv2.threshold(edges, 127, 255, cv2.THRESH_BINARY)
        binary_image_with_border = cv2.copyMakeBorder(
            binary_image, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=border_color
        )

        # Dilatación para unir regiones cercanas
        kernel = np.ones((3, 3), np.uint8)
        dilated_image = cv2.dilate(binary_image_with_border, kernel, iterations=2)

        # Etiquetar componentes conectados
        _, labels, stats, _ = cv2.connectedComponentsWithStats(
            dilated_image, connectivity=8
        )

        # Filtrar componentes por área
        area_minima = int(self.area_minima.get())
        area_maxima = int(self.area_maxima.get())

        fichas_grupos = sum(
            1 for stat in stats[1:] if area_minima < stat[4] < area_maxima
        )

        resultado = labels.astype(np.uint8) * 20

        # Redimensionar la imagen original
        max_width = 800
        max_height = 600
        resultado = self.redimensionar_imagen(resultado, max_width, max_height)

        # Visualizar etiquetas en la imagen redimensionada
        cv2.imshow("Labels", resultado)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Visualizar estadísticas
        print("Stats:", stats)

        return fichas_grupos

    def redimensionar_imagen(self, imagen_original, max_width, max_height):
        # Obtener dimensiones originales
        height, width = imagen_original.shape[:2]

        # Calcular nuevos tamaños manteniendo la proporción original
        ratio = min(max_width / width, max_height / height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)

        # Redimensionar la imagen
        imagen_redimensionada = cv2.resize(imagen_original, (new_width, new_height))

        return imagen_redimensionada
