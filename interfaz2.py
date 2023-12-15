import cv2
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from color import ContadorColor
from grupo import ContadorGrupos
from fila import ContadorFilas


class Interfaz:
    def __init__(self, root):
        self.root = root
        self.root.title("Contador de Fichas")

        # Crear un objeto Style
        style = ttk.Style()

        # Configurar el estilo del Label
        style.configure("Titulo.TLabel", background="#ffffff", font=("Helvetica", 16))

        # Título
        self.titulo_label = ttk.Label(
            self.root, text="Contador de Fichas", style="Titulo.TLabel"
        )
        self.titulo_label.grid(row=0, column=0, columnspan=4, pady=10)

        # Variables de control
        self.imagen_path = tk.StringVar()
        self.area_minima = tk.StringVar()
        self.area_maxima = tk.StringVar()
        self.color_rango_min = tk.StringVar()
        self.color_rango_max = tk.StringVar()

        # Crear widgets
        self.crear_widgets()

        # Instancia de ContadorColor
        self.contador_color = ContadorColor(
            area_minima=self.area_minima, area_maxima=self.area_maxima
        )

        # Instancia de ContadorGrupos
        self.contador_grupos = ContadorGrupos(
            area_minima=self.area_minima, area_maxima=self.area_maxima
        )

        # Instancia de ContadorFilas
        self.contador_filas = ContadorFilas(
            area_minima=self.area_minima, area_maxima=self.area_maxima
        )

    def cargar_imagen(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg")]
        )
        self.imagen_path.set(file_path)
        self.mostrar_imagen()

    def mostrar_imagen(self):
        if not self.imagen_path.get():
            messagebox.showerror(
                "Error", "Por favor, carga una imagen antes de intentar mostrarla."
            )
            return

        imagen = cv2.imread(self.imagen_path.get())
        imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        imagen_pil = Image.fromarray(imagen_rgb)

        max_width = 600
        max_height = 600
        imagen_pil.thumbnail((max_width, max_height))

        imagen_tk = ImageTk.PhotoImage(imagen_pil)

        self.imagen_label.config(image=imagen_tk)
        self.imagen_label.image = imagen_tk

    def contar_fichas(self, tipo_conteo):
        if tipo_conteo == "color":
            # Obtener valores de las variables de control
            imagen_path = self.imagen_path.get()
            color_rango = [
                int(val) for val in self.color_rango_min.get().split(",")
            ] + [int(val) for val in self.color_rango_max.get().split(",")]

            # Llamar al método de ContadorColor
            fichas_color = self.contador_color.contar_fichas_por_color(
                imagen_path, color_rango
            )

            # Muestra el resultado en un cuadro de mensaje
            mensaje = f"Cantidad de fichas del color especificado: {fichas_color}"
            messagebox.showinfo("Conteo de Fichas", mensaje)

            # Actualizar la imagen después del conteo
            self.mostrar_imagen()

        if tipo_conteo == "grupo":
            # Obtener valores de las variables de control
            imagen_path = self.imagen_path.get()
            color_rango = [
                int(val) for val in self.color_rango_min.get().split(",")
            ] + [int(val) for val in self.color_rango_max.get().split(",")]

            # Llamar al método de ContadorColor
            fichas_color = self.contador_grupos.contar_fichas_por_grupos(
                imagen_path, color_rango
            )
            # Muestra el resultado en un cuadro de mensaje
            mensaje = f"Grupo de fichas del color especificado: {fichas_color}"
            messagebox.showinfo("Conteo de Fichas", mensaje)

            # Actualizar la imagen después del conteo
            self.mostrar_imagen()

        if tipo_conteo == "filas":
            # Obtener valores de las variables de control
            imagen_path = self.imagen_path.get()
            color_rango = [
                int(val) for val in self.color_rango_min.get().split(",")
            ] + [int(val) for val in self.color_rango_max.get().split(",")]

            # Llamar al método de ContadorColor
            fichas_color = self.contador_filas.contar_fichas_por_filas(
                imagen_path, color_rango
            )
            # Muestra el resultado en un cuadro de mensaje
            mensaje = f"Fila de fichas del color especificado: {fichas_color}"
            messagebox.showinfo("Conteo de Fichas", mensaje)

            # Actualizar la imagen después del conteo
            self.mostrar_imagen()

    def crear_widgets(self):
        # Área de visualización de la imagen
        self.imagen_label = ttk.Label(self.root)
        self.imagen_label.grid(row=1, column=0, columnspan=4)

        # Botón para cargar imagen
        cargar_imagen_button = ttk.Button(
            self.root, text="Cargar Imagen", command=self.cargar_imagen
        )
        cargar_imagen_button.grid(row=2, column=0, columnspan=4, pady=10)

        # Campos de entrada para configuraciones
        ttk.Label(self.root, text="Área Mínima:").grid(row=3, column=0, pady=5)
        area_minima_entry = ttk.Entry(self.root, textvariable=self.area_minima)
        area_minima_entry.grid(row=3, column=1, pady=5)

        ttk.Label(self.root, text="Área Máxima:").grid(row=3, column=2, pady=5)
        area_maxima_entry = ttk.Entry(self.root, textvariable=self.area_maxima)
        area_maxima_entry.grid(row=3, column=3, pady=5)

        ttk.Label(self.root, text="Rango de Color Mínimo (min1,min2,min3):").grid(
            row=4, column=0, pady=5
        )
        color_rango_min_entry = ttk.Entry(self.root, textvariable=self.color_rango_min)
        color_rango_min_entry.grid(row=4, column=1, pady=5)

        ttk.Label(self.root, text="Rango de Color Máximo (max1,max2,max3):").grid(
            row=4, column=2, pady=5
        )
        color_rango_max_entry = ttk.Entry(self.root, textvariable=self.color_rango_max)
        color_rango_max_entry.grid(row=4, column=3, pady=5)

        # Botones de conteo
        contar_color_button = ttk.Button(
            self.root,
            text="Contar Fichas por Color",
            command=lambda: self.contar_fichas("color"),
        )
        contar_color_button.grid(row=5, column=0, pady=10)

        contar_grupo_button = ttk.Button(
            self.root,
            text="Contar por Grupo",
            command=lambda: self.contar_fichas("grupo"),
        )
        contar_grupo_button.grid(row=5, column=1, pady=10)

        contar_filas_button = ttk.Button(
            self.root,
            text="Contar por Filas",
            command=lambda: self.contar_fichas("filas"),
        )
        contar_filas_button.grid(row=5, column=2, pady=10)
