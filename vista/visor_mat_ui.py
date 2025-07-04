import scipy.io
import numpy as np
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog,
    QComboBox, QMessageBox, QHBoxLayout, QLineEdit
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from modelo import base_datos
import os

class VisorMatUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visor de señales .mat")
        self.setGeometry(100, 100, 900, 600)

        self.datos = {}
        self.array_actual = None

        # Layout principal
        layout = QVBoxLayout()

        # Botón para cargar archivo .mat
        self.boton_cargar = QPushButton("Cargar archivo .mat")
        self.boton_cargar.clicked.connect(self.cargar_mat)
        layout.addWidget(self.boton_cargar)

        # ComboBox para elegir la llave
        self.combo_llaves = QComboBox()
        self.combo_llaves.currentTextChanged.connect(self.verificar_llave)
        layout.addWidget(QLabel("Seleccionar variable:"))
        layout.addWidget(self.combo_llaves)

        # Inputs para canales
        h1 = QHBoxLayout()
        self.input_canal_i = QLineEdit()
        self.input_canal_f = QLineEdit()
        h1.addWidget(QLabel("Canal inicial:"))
        h1.addWidget(self.input_canal_i)
        h1.addWidget(QLabel("Canal final:"))
        h1.addWidget(self.input_canal_f)
        layout.addLayout(h1)

        # Inputs para intervalo
        h2 = QHBoxLayout()
        self.input_tiempo_i = QLineEdit()
        self.input_tiempo_f = QLineEdit()
        h2.addWidget(QLabel("Tiempo inicial:"))
        h2.addWidget(self.input_tiempo_i)
        h2.addWidget(QLabel("Tiempo final:"))
        h2.addWidget(self.input_tiempo_f)
        layout.addLayout(h2)

        # Botones de acción
        self.boton_graficar = QPushButton("Graficar segmento")
        self.boton_promedio = QPushButton("Mostrar promedio eje 1")
        self.boton_graficar.clicked.connect(self.graficar_segmento)
        self.boton_promedio.clicked.connect(self.graficar_promedio)

        layout.addWidget(self.boton_graficar)
        layout.addWidget(self.boton_promedio)

        # Canvas de Matplotlib
        self.canvas = FigureCanvas(plt.figure())
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def cargar_mat(self):
        archivo, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo .mat", "", "Archivos mat (*.mat)")
        if archivo:
            self.datos = scipy.io.loadmat(archivo)
            llaves = [k for k in self.datos.keys() if not k.startswith("__")]
            self.combo_llaves.clear()
            self.combo_llaves.addItems(llaves)

            # Registrar en la base de datos
            nombre = os.path.basename(archivo)
            base_datos.registrar_archivo("mat", nombre, archivo)

    def verificar_llave(self):
        llave = self.combo_llaves.currentText()
        if llave:
            array = self.datos[llave]
            if isinstance(array, np.ndarray):
                self.array_actual = array
                self.graficar_todo()
            else:
                QMessageBox.warning(self, "Error", "La variable seleccionada no es un arreglo. Intente con otra.")
                self.array_actual = None

    def graficar_todo(self):
        if self.array_actual is not None:
            self.canvas.figure.clf()
            ax = self.canvas.figure.add_subplot(111)

            n_canales = self.array_actual.shape[0]
            desplazamiento = np.max(np.abs(self.array_actual)) * 1.2  # espacio entre señales

            for i in range(n_canales):
                offset = i * desplazamiento
                ax.plot(self.array_actual[i] + offset, label=f"Canal {i}")

            ax.set_title("Señales apiladas verticalmente")
            ax.set_xlabel("Tiempo")
            ax.set_ylabel("Canales desplazados")
            ax.set_yticks([i * desplazamiento for i in range(n_canales)])
            ax.set_yticklabels([f"Canal {i}" for i in range(n_canales)])
            ax.invert_yaxis()  # opcional: del canal 0 arriba al último abajo
            self.canvas.figure.tight_layout()
            self.canvas.draw()

    def graficar_segmento(self):
        if self.array_actual is None:
            return

        try:
            i = int(self.input_canal_i.text())
            f = int(self.input_canal_f.text())
            t0 = int(self.input_tiempo_i.text())
            t1 = int(self.input_tiempo_f.text())

            self.canvas.figure.clf()
            ax = self.canvas.figure.add_subplot(111)

            for canal in range(i, f + 1):
                if canal < self.array_actual.shape[0]:
                    ax.plot(self.array_actual[canal, t0:t1], label=f"Canal {canal}")

            ax.set_title("Segmento de canales")
            ax.set_xlabel("Tiempo")
            ax.set_ylabel("Amplitud")
            ax.legend()
            self.canvas.draw()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Datos inválidos: {e}")

    def graficar_promedio(self):
        if self.array_actual is None:
            return

        promedio = np.mean(self.array_actual, axis=1)  # promedio por canal
        x = np.arange(len(promedio))  # eje X: 0 a N-1

        self.canvas.figure.clf()
        ax = self.canvas.figure.add_subplot(111)
        ax.stem(x, promedio, use_line_collection=True)
        ax.set_title("Promedio a lo largo del eje 1")
        ax.set_xlabel("Canal")
        ax.set_ylabel("Promedio")
        self.canvas.draw()