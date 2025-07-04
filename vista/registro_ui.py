from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox, QMessageBox
)
from modelo import base_datos

class RegistroUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Crear nuevo usuario")

        self.label_user = QLabel("Nuevo usuario")
        self.input_user = QLineEdit()

        self.label_pass = QLabel("Contraseña")
        self.input_pass = QLineEdit()
        self.input_pass.setEchoMode(QLineEdit.Password)

        self.label_rol = QLabel("Rol")
        self.combo_rol = QComboBox()
        self.combo_rol.addItems(["imagen", "senal"])

        self.boton_registrar = QPushButton("Registrar")
        self.boton_registrar.clicked.connect(self.registrar_usuario)

        layout = QVBoxLayout()
        layout.addWidget(self.label_user)
        layout.addWidget(self.input_user)
        layout.addWidget(self.label_pass)
        layout.addWidget(self.input_pass)
        layout.addWidget(self.label_rol)
        layout.addWidget(self.combo_rol)
        layout.addWidget(self.boton_registrar)

        self.setLayout(layout)

    def registrar_usuario(self):
        user = self.input_user.text()
        pw = self.input_pass.text()
        rol = self.combo_rol.currentText()

        if user == "" or pw == "":
            QMessageBox.warning(self, "Campos vacíos", "Debes llenar todos los campos.")
            return

        resultado = base_datos.insertar_usuario(user, pw, rol)
        if resultado:
            QMessageBox.information(self, "Éxito", "Usuario registrado correctamente.")
            self.close()
        else:
            QMessageBox.critical(self, "Error", "Ese usuario ya existe.")