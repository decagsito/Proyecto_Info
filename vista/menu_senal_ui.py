from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class MenuSenalUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menú - Experto en Señales")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Bienvenido al módulo de señales"))
        self.setLayout(layout)