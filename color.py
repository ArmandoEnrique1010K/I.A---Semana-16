import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk


class ContadorColor:
    def __init__(self, area_minima, area_maxima):
        # Variables de control
        self.color_rango = None
        self.resultado_label_text = None
        self.area_minima = area_minima
        self.area_maxima = area_maxima

    def contar_fichas_por_color(self, imagen_path, color_rango):
        # Lógica para contar fichas por color
        imagen = cv2.imread(imagen_path)
        imagen_hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

        # Obtener el rango de color especificado por el usuario
        color_min = np.array(color_rango[:3], np.uint8)
        color_max = np.array(color_rango[3:], np.uint8)

        # Crear la máscara
        mask_color = cv2.inRange(imagen_hsv, color_min, color_max)

        # Aplicar la máscara sobre la imagen original
        resultado = cv2.bitwise_and(imagen, imagen, mask=mask_color)

        # Encontrar contornos en la máscara
        contornos_color, _ = cv2.findContours(
            mask_color, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        # Establecer áreas mínima y máxima para contar
        area_minima = int(self.area_minima.get())
        area_maxima = int(self.area_maxima.get())
        fichas_color = sum(
            1
            for contorno in contornos_color
            if area_minima < cv2.contourArea(contorno) < area_maxima
        )
        max_width = 800
        max_height = 600
        resultado = self.redimensionar_imagen(resultado, max_width, max_height)

        # Muestra el resultado
        cv2.imshow("Resultado", resultado)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return fichas_color

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
