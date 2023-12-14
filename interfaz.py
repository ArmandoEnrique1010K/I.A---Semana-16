import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from funcion_contar_por_color import contar_fichas_por_color  # Importa la función
from funcion_contar_por_grupo import contar_fichas_por_grupo  # Importa la función
import numpy as np


# Definir rangos de colores en formato HSV
rango_color_rojo = ([0, 100, 100], [10, 255, 255])
rango_color_verde = ([40, 100, 100], [80, 255, 255])
rango_color_azul = ([100, 100, 100], [140, 255, 255])
rango_color_amarillo = ([20, 100, 100], [30, 255, 255])
rango_color_naranja = ([10, 100, 100], [20, 255, 255])
rango_color_morado = ([120, 100, 100], [160, 255, 255])
rango_color_negro = ([0, 0, 0], [180, 255, 30])
rango_color_blanco = ([0, 0, 200], [180, 20, 255])


class Interfaz:
    def __init__(self, root):
        # Crea la interfaz de la ventana grafica
        self.root = root
        self.root.title("Contador de Fichas")

        # Titulo
        self.titulo_label = tk.Label(
            root,
            text="Contador de Fichas",
            font=("Arial", 20),
            bg="#005923",
            fg="#ffffff",
        )
        self.titulo_label.pack(pady=10, fill="both", expand=False, anchor="center")

        # Campo para mostrar la imagen
        self.label_imagen = tk.Label(root, height=0)
        self.label_imagen.pack(pady=10, fill="both", expand=False, anchor="center")

        # Boton para subir la imagen
        self.cargar_imagen_btn = tk.Button(
            root, text="Subir Imagen", command=self.cargar_imagen
        )
        self.cargar_imagen_btn.pack(pady=5)

        # Crear un contenedor para los botones
        self.botones_frame = tk.Frame(root)
        self.botones_frame.pack()
        # BOTONES PARA CONTAR POR COLORES
        botones_colores = [
            ("Rojo", rango_color_rojo),
            ("Azul", rango_color_azul),
            ("Verde", rango_color_verde),
            ("Amarillo", rango_color_amarillo),
            ("Naranja", rango_color_naranja),
            ("Morado", rango_color_morado),
            ("Negro", rango_color_negro),
            ("Blanco", rango_color_blanco),
        ]
        for nombre_color, rango_color in botones_colores:
            boton_color = tk.Button(
                self.botones_frame,
                text=f"Contar {nombre_color}",
                command=lambda rc=rango_color: self.contar_por_color(rc),
            )
            boton_color.pack(side=tk.LEFT, padx=5)

        self.contar_grupo_btn = tk.Button(
            root, text="Contar por Grupo", command=self.contar_por_grupo
        )
        self.contar_grupo_btn.pack(pady=5)

        self.contar_fila_btn = tk.Button(
            root, text="Contar por Fila", command=self.contar_por_fila
        )
        self.contar_fila_btn.pack(pady=5)

        self.resultado_text = tk.Text(root, height=5, width=50)
        self.resultado_text.pack(pady=10)

    def cargar_imagen(self):
        path = filedialog.askopenfilename()
        if path:
            self.imagen_original = cv2.imread(path)
            self.mostrar_imagen(self.imagen_original)

    def contar_por_color(self, rango_color):
        if hasattr(self, "imagen_original"):
            # Llama a la función contar_fichas_por_color con el rango de color proporcionado
            resultado, num_fichas = contar_fichas_por_color(
                self.imagen_original, rango_color
            )

            # Muestra la imagen resultante
            self.mostrar_imagen(resultado, ancho_maximo=500, altura_maxima=500)

            # Muestra el resultado en el cuadro de texto
            self.mostrar_resultado(f"Número de fichas: {num_fichas}")

    def contar_por_grupo(self):
        if hasattr(self, "imagen_original"):
            # Llama a la función contar_fichas_por_color con el rango de color proporcionado
            resultado, num_grupos_fichas = contar_fichas_por_grupo(self.imagen_original)

            # Muestra la imagen resultante
            self.mostrar_imagen_contar_por_grupo(
                resultado, ancho_maximo=500, altura_maxima=500
            )

            # Muestra el resultado en el cuadro de texto
            self.mostrar_resultado(f"Número de grupos: {num_grupos_fichas}")
        else:
            print("funcion")
        pass

    def contar_por_fila(self):
        # Implementa el código para contar fichas por fila
        # Actualiza self.imagen_procesada con el resultado
        # Muestra la imagen procesada en la interfaz
        # Actualiza el cuadro de texto con el resultado
        pass

    def mostrar_imagen(self, img, ancho_maximo=500, altura_maxima=500):
        shape = img.shape
        print(f"Shape de la imagen: {shape}")
        if len(shape) == 3:
            alto_original, ancho_original, _ = shape
        else:
            alto_original, ancho_original = shape[:2]

        # Calcula las nuevas dimensiones respetando tanto el ancho máximo como la altura máxima
        ratio_ancho = ancho_maximo / ancho_original
        ratio_alto = altura_maxima / alto_original

        # Utiliza el ratio más pequeño para asegurar que la imagen mantenga su relación de aspecto
        ratio = min(ratio_ancho, ratio_alto)

        # Calcula las nuevas dimensiones
        nuevo_ancho = int(ancho_original * ratio)
        nuevo_alto = int(alto_original * ratio)

        # Redimensiona la imagen
        img_redimensionada = cv2.resize(
            img, (nuevo_ancho, nuevo_alto), interpolation=cv2.INTER_AREA
        )

        # Convierte a formato compatible con tkinter
        img_redimensionada = cv2.cvtColor(img_redimensionada, cv2.COLOR_BGR2RGB)
        img_redimensionada = Image.fromarray(img_redimensionada)
        img_redimensionada = ImageTk.PhotoImage(img_redimensionada)

        # Configura la etiqueta de la imagen en la interfaz
        self.label_imagen.configure(image=img_redimensionada)
        self.label_imagen.image = img_redimensionada

    def mostrar_imagen_contar_por_grupo(self, img, ancho_maximo=500, altura_maxima=500):
        # Inicializa las variables fuera del bloque condicional
        alto_original, ancho_original = 0, 0

        if isinstance(img, np.ndarray):
            shape = img.shape
            print(f"Shape de la imagen: {shape}")
            if len(shape) == 3:
                alto_original, ancho_original, _ = shape
            else:
                alto_original, ancho_original = shape[:2]

        # Continuación del código...
        ratio_ancho = ancho_maximo / ancho_original if ancho_original != 0 else 1
        ratio_alto = altura_maxima / alto_original if alto_original != 0 else 1

        # Utiliza el ratio más pequeño para asegurar que la imagen mantenga su relación de aspecto
        ratio = min(ratio_ancho, ratio_alto)

        # Calcula las nuevas dimensiones
        nuevo_ancho = int(ancho_original * ratio)
        nuevo_alto = int(alto_original * ratio)
        # Redimensiona la imagen
        img_redimensionada = cv2.resize(
            img, (nuevo_ancho, nuevo_alto), interpolation=cv2.INTER_AREA
        )

        # Convierte a formato compatible con tkinter
        img_redimensionada = cv2.cvtColor(img_redimensionada, cv2.COLOR_BGR2RGB)
        img_redimensionada = Image.fromarray(img_redimensionada)
        img_redimensionada = ImageTk.PhotoImage(img_redimensionada)

        # Configura la etiqueta de la imagen en la interfaz
        self.label_imagen.configure(image=img_redimensionada)
        self.label_imagen.image = img_redimensionada

    def mostrar_resultado(self, resultado):
        self.resultado_text.delete(1.0, tk.END)  # Limpiar el cuadro de texto

        # Convertir el resultado a una cadena antes de insertarlo
        resultado_str = str(resultado)

        self.resultado_text.insert(tk.END, resultado_str)
