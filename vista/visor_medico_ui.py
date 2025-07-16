import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFileDialog, QSlider, QLabel, QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from modelo.dicom_nifti import cargar_dicom_carpeta, cargar_nifti, dicom_a_nifti
from modelo import base_datos


class VisorMedicoUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visor Médico - BioAnalyser")
        self.volumen = None

        layout = QVBoxLayout()

        # Botones de carga
        btn_cargar_dicom = QPushButton("Cargar carpeta DICOM")
        btn_cargar_nifti = QPushButton("Cargar archivo NIfTI")
        btn_cargar_dicom.clicked.connect(self.cargar_dicom)
        btn_cargar_nifti.clicked.connect(self.cargar_nifti)
        btn_convertir = QPushButton("Convertir carpeta DICOM a NIfTI")
        btn_convertir.clicked.connect(self.convertir_dicom_nifti)

        layout.addWidget(btn_convertir)
        layout.addWidget(btn_cargar_dicom)
        layout.addWidget(btn_cargar_nifti)

        # Canvas de matplotlib
        self.fig, self.axs = plt.subplots(1, 3, figsize=(12, 4))
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        # Sliders
        self.sliders = []
        nombres = ["Axial (Z)", "Coronal (Y)", "Sagital (X)"]
        for i in range(3):
            h = QHBoxLayout()
            h.addWidget(QLabel(nombres[i]))
            slider = QSlider(Qt.Horizontal)
            slider.valueChanged.connect(self.actualizar_vista)
            slider.setEnabled(False)
            h.addWidget(slider)
            self.sliders.append(slider)
            layout.addLayout(h)

        self.setLayout(layout)

    def cargar_dicom(self):
        carpeta = QFileDialog.getExistingDirectory(self, "Selecciona carpeta DICOM")
        if carpeta:
            self.volumen = cargar_dicom_carpeta(carpeta)
            self.configurar_sliders()

    def cargar_nifti(self):
        archivo, _ = QFileDialog.getOpenFileName(self, "Selecciona archivo NIfTI", filter="*.nii *.nii.gz")
        if archivo:
            self.volumen = cargar_nifti(archivo)
            self.configurar_sliders()

    def cargar_dicom_desde_ruta(self, ruta):
        try:
            self.volumen = cargar_dicom_carpeta(ruta)
            self.configurar_sliders()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar el DICOM desde la ruta:\n{e}")

    def configurar_sliders(self):
        if self.volumen is None:
            return
        dims = self.volumen.shape
        for i, slider in enumerate(self.sliders):
            slider.setMaximum(dims[i] - 1)
            slider.setValue(dims[i] // 2)
            slider.setEnabled(True)
        self.actualizar_vista()

    def actualizar_vista(self):
        if self.volumen is None:
            return

        idx_axial = self.sliders[0].value()
        idx_coronal = self.sliders[1].value()
        idx_sagital = self.sliders[2].value()

        # Obtener slices
        axial = self.volumen[idx_axial, :, :]
        coronal = self.volumen[:, idx_coronal, :]
        sagital = self.volumen[:, :, idx_sagital]

        slices = [axial, coronal, sagital]
        titles = ["Axial", "Coronal", "Sagital"]

        for ax, img, title in zip(self.axs, slices, titles):
            ax.clear()
            img = np.rot90(img)  # Asegurar orientación estándar
            ax.imshow(img, cmap='gray', aspect='auto')
            ax.set_title(title)
            ax.axis('off')

        self.fig.tight_layout()
        self.canvas.draw()

    def convertir_dicom_nifti(self):
        carpeta = QFileDialog.getExistingDirectory(self, "Selecciona carpeta DICOM")
        if carpeta:
            nombre_salida = QFileDialog.getSaveFileName(self, "Guardar NIfTI como", filter="*.nii.gz")[0]
            if nombre_salida:
                nifti_path = dicom_a_nifti(carpeta, nombre_salida)
                base_datos.registrar_conversion_dicom_a_nifti(carpeta, nifti_path)
                QMessageBox.information(self, "Éxito", "Conversión y guardado exitosos.")