import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QTabWidget, QHBoxLayout, QMessageBox
)
from modelo import base_datos
from vista.visor_mat_ui import VisorMatUI
from vista.visor_csv_ui import VisorCSVUI
from vista.procesador_jpg_ui import ProcesadorJPGUI
from vista.visor_medico_ui import VisorMedicoUI

class HistorialUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Historial de archivos procesados")
        self.setGeometry(150, 150, 850, 500)
        self.ventana_activa = None

        layout = QVBoxLayout()

        self.tabs = QTabWidget()

        # === TAB DICOM / NIFTI ===
        self.tab_dicom = QWidget()
        self.tabla_dicom = QTableWidget()
        dicom_layout = QVBoxLayout()
        dicom_layout.addWidget(QLabel("Archivos DICOM / NIfTI"))
        dicom_layout.addWidget(self.tabla_dicom)

        # Botones de acciones para DICOM
        btns_dicom = QHBoxLayout()
        btn_actualizar_dicom = QPushButton("Actualizar")
        btn_abrir_dicom = QPushButton("Abrir archivo NIfTI")
        btn_actualizar_dicom.clicked.connect(self.cargar_dicom)
        btn_abrir_dicom.clicked.connect(self.abrir_dicom)
        btns_dicom.addWidget(btn_actualizar_dicom)
        btns_dicom.addWidget(btn_abrir_dicom)
        dicom_layout.addLayout(btns_dicom)

        self.tab_dicom.setLayout(dicom_layout)
        self.tabs.addTab(self.tab_dicom, "Imágenes médicas")

        # === TAB ARCHIVOS (jpg, png, mat, csv) ===
        self.tab_otros = QWidget()
        self.tabla_otros = QTableWidget()
        otros_layout = QVBoxLayout()
        otros_layout.addWidget(QLabel("Archivos JPG / PNG / MAT / CSV"))
        otros_layout.addWidget(self.tabla_otros)

        # Botones de acciones para otros archivos
        btns_otros = QHBoxLayout()
        btn_actualizar_otros = QPushButton("Actualizar")
        btn_abrir_otros = QPushButton("Abrir archivo")
        btn_actualizar_otros.clicked.connect(self.cargar_otros)
        btn_abrir_otros.clicked.connect(self.abrir_otros)
        btns_otros.addWidget(btn_actualizar_otros)
        btns_otros.addWidget(btn_abrir_otros)
        otros_layout.addLayout(btns_otros)

        self.tab_otros.setLayout(otros_layout)
        self.tabs.addTab(self.tab_otros, "Otros archivos")

        layout.addWidget(self.tabs)

        # Botón cerrar
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(self.close)
        layout.addWidget(btn_cerrar)

        self.setLayout(layout)

        # Cargar al inicio
        self.cargar_dicom()
        self.cargar_otros()

    def cargar_dicom(self):
        datos = base_datos.obtener_dicom_nifti()
        self.tabla_dicom.setRowCount(len(datos))
        self.tabla_dicom.setColumnCount(4)
        self.tabla_dicom.setHorizontalHeaderLabels(["Tipo", "Ruta DICOM", "Ruta NIfTI", "Fecha"])
        for i, fila in enumerate(datos):
            for j, valor in enumerate(fila):
                self.tabla_dicom.setItem(i, j, QTableWidgetItem(str(valor)))
        self.tabla_dicom.resizeColumnsToContents()

    def cargar_otros(self):
        datos = base_datos.obtener_archivos()
        self.tabla_otros.setRowCount(len(datos))
        self.tabla_otros.setColumnCount(4)
        self.tabla_otros.setHorizontalHeaderLabels(["Tipo", "Nombre", "Ruta", "Fecha"])
        for i, fila in enumerate(datos):
            for j, valor in enumerate(fila):
                self.tabla_otros.setItem(i, j, QTableWidgetItem(str(valor)))
        self.tabla_otros.resizeColumnsToContents()

    def abrir_dicom(self):
        fila = self.tabla_dicom.currentRow()
        if fila != -1:
            ruta_nifti = self.tabla_dicom.item(fila, 2).text()
            self.abrir_archivo(ruta_nifti)
        else:
            QMessageBox.warning(self, "Aviso", "Seleccione un archivo NIfTI para abrir.")

    def abrir_otros(self):
        fila = self.tabla_otros.currentRow()
        if fila != -1:
            ruta = self.tabla_otros.item(fila, 2).text()
            self.abrir_archivo(ruta)
        else:
            QMessageBox.warning(self, "Aviso", "Seleccione un archivo para abrir.")

    def abrir_archivo(self, ruta):
        if not os.path.exists(ruta):
            QMessageBox.warning(self, "Archivo no encontrado", "La ruta especificada no existe.")
            return

        extension = os.path.splitext(ruta)[1].lower()

        try:
            if extension == ".mat":                
                self.ventana_activa = VisorMatUI()
                self.ventana_activa.show()
                self.ventana_activa.cargar_mat_desde_ruta(ruta)

            elif extension == ".csv":                
                self.ventana_activa = VisorCSVUI()
                self.ventana_activa.show()
                self.ventana_activa.cargar_csv_desde_ruta(ruta)

            elif extension in [".jpg", ".png"]:                
                self.ventana_activa = ProcesadorJPGUI()
                self.ventana_activa.show()
                self.ventana_activa.cargar_imagen_desde_ruta(ruta)

            elif extension == ".dcm":
                self.ventana_activa = VisorMedicoUI()
                self.ventana_activa.show()
                self.ventana_activa.cargar_dicom_desde_ruta(ruta)

            else:
                # como fallback abrir en el sistema
                if os.name == 'nt':
                    os.startfile(ruta)
                else:
                    import subprocess
                    subprocess.Popen(['xdg-open', ruta])

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo abrir el archivo:\n{e}")