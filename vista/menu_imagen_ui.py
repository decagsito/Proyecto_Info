from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class MenuImagenUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menú - Experto en Imágenes")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Bienvenido al módulo de imágenes"))
        self.setLayout(layout)