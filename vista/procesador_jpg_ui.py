import cv2
import numpy as np
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout,
    QFileDialog, QComboBox, QSlider, QSpinBox
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import os
from modelo import base_datos

class ProcesadorJPGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Procesador de Imágenes JPG/PNG")
        self.setGeometry(100, 100, 900, 600)

        self.imagen_original = None
        self.imagen_procesada = None

        # Widgets
        self.boton_cargar = QPushButton("Cargar Imagen")
        self.boton_cargar.clicked.connect(self.cargar_imagen)

        self.combo_procesos = QComboBox()
        self.combo_procesos.addItems([
            "Cambio de espacio de color",
            "Ecualización",
            "Binarización",
            "Apertura",
            "Cierre",
            "Conteo de células",
            "Detección de bordes (Canny)"
        ])
        self.combo_procesos.currentTextChanged.connect(self.aplicar_proceso)

        self.kernel_slider = QSlider(Qt.Horizontal)
        self.kernel_slider.setMinimum(1)
        self.kernel_slider.setMaximum(21)
        self.kernel_slider.setValue(3)
        self.kernel_slider.setSingleStep(2)
        self.kernel_slider.valueChanged.connect(self.aplicar_proceso)

        self.canvas = FigureCanvas(plt.figure(figsize=(8, 4)))

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.boton_cargar)
        layout.addWidget(QLabel("Seleccione proceso"))
        layout.addWidget(self.combo_procesos)
        layout.addWidget(QLabel("Tamaño de kernel"))
        layout.addWidget(self.kernel_slider)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def cargar_imagen(self):
        ruta, _ = QFileDialog.getOpenFileName(self, "Seleccionar imagen", "", "Imagenes (*.jpg *.png)")
        if ruta:
            self.imagen_original = cv2.imread(ruta, cv2.IMREAD_COLOR)
            self.imagen_procesada = self.imagen_original.copy()
            self.mostrar_imagenes()

            # Guardar en base de datos
            tipo = os.path.splitext(ruta)[1].replace(".", "").lower()  # 'jpg' o 'png'
            nombre = os.path.basename(ruta)
            base_datos.registrar_archivo(tipo, nombre, ruta)

    def aplicar_proceso(self):
        if self.imagen_original is None:
            return

        img = self.imagen_original.copy()
        proceso = self.combo_procesos.currentText()
        k = self.kernel_slider.value()
        k = k if k % 2 != 0 else k + 1  # kernel impar

        if proceso == "Cambio de espacio de color":
            img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        elif proceso == "Ecualización":
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = cv2.equalizeHist(img_gray)
        elif proceso == "Binarización":
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, img = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
        elif proceso == "Apertura":
            kernel = np.ones((k, k), np.uint8)
            img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        elif proceso == "Cierre":
            kernel = np.ones((k, k), np.uint8)
            img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        elif proceso == "Conteo de células":
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            img = cv2.drawContours(img.copy(), contours, -1, (0, 255, 0), 2)
            print(f"Células detectadas: {len(contours)}")
        elif proceso == "Detección de bordes (Canny)":
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = cv2.Canny(img_gray, 50, 150)

        self.imagen_procesada = img
        self.mostrar_imagenes()

    def mostrar_imagenes(self):
        if self.imagen_original is None or self.imagen_procesada is None:
            return

        self.canvas.figure.clf()
        ax1 = self.canvas.figure.add_subplot(1, 2, 1)
        ax2 = self.canvas.figure.add_subplot(1, 2, 2)

        if len(self.imagen_original.shape) == 2:
            ax1.imshow(self.imagen_original, cmap='gray')
        else:
            ax1.imshow(cv2.cvtColor(self.imagen_original, cv2.COLOR_BGR2RGB))
        ax1.set_title("Original")
        ax1.axis('off')

        if len(self.imagen_procesada.shape) == 2:
            ax2.imshow(self.imagen_procesada, cmap='gray')
        else:
            ax2.imshow(cv2.cvtColor(self.imagen_procesada, cv2.COLOR_BGR2RGB))
        ax2.set_title("Procesada")
        ax2.axis('off')

        self.canvas.draw()