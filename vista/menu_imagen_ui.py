from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from vista.visor_medico_ui import VisorMedicoUI
from vista.procesador_jpg_ui import ProcesadorJPGUI
from vista.historial_ui import HistorialUI

class MenuImagenUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menú - Experto en Imágenes")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Bienvenido al módulo de imágenes biomédicas"))

        # Botón para visor DICOM/NIfTI
        btn_visor_medico = QPushButton("Visualizar imágenes médicas")
        btn_visor_medico.clicked.connect(self.abrir_visor)
        layout.addWidget(btn_visor_medico)

        # Botón para procesamiento JPG/PNG (se implementará luego)
        btn_jpg_png = QPushButton("Procesar imágenes JPG/PNG")
        btn_jpg_png.clicked.connect(self.procesar_jpg_png)  # Temporal
        layout.addWidget(btn_jpg_png)

        # botón para ver historial
        btn_historial = QPushButton("Ver historial de archivos")
        btn_historial.clicked.connect(self.abrir_historial)
        layout.addWidget(btn_historial)

        # Botón para salir (cerrar ventana o volver al login)
        btn_salir = QPushButton("Cerrar sesión")
        btn_salir.clicked.connect(self.close)
        layout.addWidget(btn_salir)

        self.setLayout(layout)


    def abrir_visor(self):
        self.visor = VisorMedicoUI()
        self.visor.show()

    def procesar_jpg_png(self):
        self.proc = ProcesadorJPGUI()
        self.proc.show()

    def abrir_historial(self):
        self.historial = HistorialUI()
        self.historial.show()