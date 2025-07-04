from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton
)
from PyQt5.QtGui import QFont
from vista.historial_ui import HistorialUI
from vista.visor_mat_ui import VisorMatUI
from vista.visor_csv_ui import VisorCSVUI

class MenuSenalUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menú - Experto en Señales")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()

        titulo = QLabel("Bienvenido al módulo de señales biomédicas")
        titulo.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(titulo)

        # Botón para cargar y analizar .mat
        btn_mat = QPushButton("Visualizar señales (.mat)")
        btn_mat.clicked.connect(self.abrir_mat)
        layout.addWidget(btn_mat)

        # Botón para cargar y visualizar CSV
        btn_csv = QPushButton("Visualizar datos tabulares (.csv)")
        btn_csv.clicked.connect(self.abrir_csv)
        layout.addWidget(btn_csv)

        # Botón para ver historial
        btn_historial = QPushButton("Ver historial de archivos")
        btn_historial.clicked.connect(self.abrir_historial)
        layout.addWidget(btn_historial)

        # Botón para salir
        btn_salir = QPushButton("Cerrar sesión")
        btn_salir.clicked.connect(self.close)
        layout.addWidget(btn_salir)

        self.setLayout(layout)

    def abrir_mat(self):
        self.mat = VisorMatUI()
        self.mat.show()

    def abrir_csv(self):
        self.csv = VisorCSVUI()
        self.csv.show()

    def abrir_historial(self):
        self.historial = HistorialUI()
        self.historial.show()