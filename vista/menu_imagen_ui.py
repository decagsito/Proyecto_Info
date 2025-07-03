from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from vista.visor_medico_ui import VisorMedicoUI

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

        # Botón para salir (cerrar ventana o volver al login)
        btn_salir = QPushButton("Cerrar sesión")
        btn_salir.clicked.connect(self.close)
        layout.addWidget(btn_salir)

        self.setLayout(layout)

    def abrir_visor(self):
        self.visor = VisorMedicoUI()
        self.visor.show()

    def procesar_jpg_png(self):
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self, "Próximamente", "Este módulo se implementará luego.")