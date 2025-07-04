import pandas as pd
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFileDialog,
    QTableWidget, QTableWidgetItem, QLabel, QComboBox, QMessageBox
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import os
from modelo import base_datos

class VisorCSVUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visualizador de archivos CSV")
        self.setGeometry(150, 150, 800, 600)

        self.df = None

        # Layout principal
        layout = QVBoxLayout()

        # Botón para cargar CSV
        btn_cargar = QPushButton("Cargar archivo CSV")
        btn_cargar.clicked.connect(self.cargar_csv)
        layout.addWidget(btn_cargar)

        # Tabla
        self.tabla = QTableWidget()
        layout.addWidget(self.tabla)

        # Selección de columnas
        layout.addWidget(QLabel("Selecciona columnas para graficar:"))
        self.combo_x = QComboBox()
        self.combo_y = QComboBox()
        layout.addWidget(self.combo_x)
        layout.addWidget(self.combo_y)

        # Botón graficar
        btn_graficar = QPushButton("Graficar scatter")
        btn_graficar.clicked.connect(self.graficar)
        layout.addWidget(btn_graficar)

        # Área de gráfico
        self.canvas = FigureCanvas(plt.figure())
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def cargar_csv(self):
        ruta, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo CSV", "", "CSV (*.csv)")
        if ruta:
            try:
                self.df = pd.read_csv(ruta)
                self.mostrar_tabla()
                columnas = list(self.df.columns)
                self.combo_x.clear()
                self.combo_y.clear()
                self.combo_x.addItems(columnas)
                self.combo_y.addItems(columnas)

                # Guardar en base de datos
                nombre = os.path.basename(ruta)
                base_datos.registrar_archivo("csv", nombre, ruta)

            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo cargar el archivo: {e}")

    def mostrar_tabla(self):
        self.tabla.setRowCount(len(self.df))
        self.tabla.setColumnCount(len(self.df.columns))
        self.tabla.setHorizontalHeaderLabels(self.df.columns)

        for i in range(len(self.df)):
            for j in range(len(self.df.columns)):
                valor = str(self.df.iat[i, j])
                self.tabla.setItem(i, j, QTableWidgetItem(valor))

    def graficar(self):
        if self.df is None:
            return

        col_x = self.combo_x.currentText()
        col_y = self.combo_y.currentText()

        try:
            self.canvas.figure.clf()
            ax = self.canvas.figure.add_subplot(111)
            ax.scatter(self.df[col_x], self.df[col_y], alpha=0.7)
            ax.set_xlabel(col_x)
            ax.set_ylabel(col_y)
            ax.set_title(f"{col_y} vs {col_x}")
            self.canvas.draw()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo graficar: {e}")