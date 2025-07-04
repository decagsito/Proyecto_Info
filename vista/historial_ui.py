from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QTabWidget
from modelo import base_datos

class HistorialUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Historial de archivos procesados")
        self.setGeometry(150, 150, 800, 500)

        layout = QVBoxLayout()

        tabs = QTabWidget()

        # Tab 1: Imágenes médicas
        self.tab_dicom = QWidget()
        self.tab_dicom_layout = QVBoxLayout()
        self.tabla_dicom = QTableWidget()
        self.tab_dicom_layout.addWidget(QLabel("DICOM / NIfTI"))
        self.tab_dicom_layout.addWidget(self.tabla_dicom)
        self.tab_dicom.setLayout(self.tab_dicom_layout)

        # Tab 2: Otros archivos (jpg, png, mat, csv)
        self.tab_otros = QWidget()
        self.tab_otros_layout = QVBoxLayout()
        self.tabla_otros = QTableWidget()
        self.tab_otros_layout.addWidget(QLabel("JPG / PNG / MAT / CSV"))
        self.tab_otros_layout.addWidget(self.tabla_otros)
        self.tab_otros.setLayout(self.tab_otros_layout)

        tabs.addTab(self.tab_dicom, "Imágenes médicas")
        tabs.addTab(self.tab_otros, "Otros archivos")

        layout.addWidget(tabs)

        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(self.close)
        layout.addWidget(btn_cerrar)

        self.setLayout(layout)
        self.cargar_datos()

    def cargar_datos(self):
        # Datos imágenes médicas
        datos_dicom = base_datos.obtener_dicom_nifti()
        self.tabla_dicom.setColumnCount(4)
        self.tabla_dicom.setHorizontalHeaderLabels(["Tipo", "Ruta DICOM", "Ruta NIfTI", "Fecha"])
        self.tabla_dicom.setRowCount(len(datos_dicom))
        for i, fila in enumerate(datos_dicom):
            for j, valor in enumerate(fila):
                self.tabla_dicom.setItem(i, j, QTableWidgetItem(str(valor)))

        # Datos otros archivos
        datos_otros = base_datos.obtener_archivos()
        self.tabla_otros.setColumnCount(4)
        self.tabla_otros.setHorizontalHeaderLabels(["Tipo", "Nombre", "Ruta", "Fecha"])
        self.tabla_otros.setRowCount(len(datos_otros))
        for i, fila in enumerate(datos_otros):
            for j, valor in enumerate(fila):
                self.tabla_otros.setItem(i, j, QTableWidgetItem(str(valor)))