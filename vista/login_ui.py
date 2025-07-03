from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox

class LoginUI(QWidget):
    def __init__(self, controlador):
        super().__init__()
        self.controlador = controlador
        self.setWindowTitle("Login - BioAnalyser")
        self.setGeometry(100, 100, 300, 150)

        self.label_user = QLabel("Usuario")
        self.input_user = QLineEdit()

        self.label_pass = QLabel("Contraseña")
        self.input_pass = QLineEdit()
        self.input_pass.setEchoMode(QLineEdit.Password)

        self.boton_login = QPushButton("Ingresar")
        self.boton_login.clicked.connect(self.login)

        layout = QVBoxLayout()
        layout.addWidget(self.label_user)
        layout.addWidget(self.input_user)
        layout.addWidget(self.label_pass)
        layout.addWidget(self.input_pass)
        layout.addWidget(self.boton_login)

        self.setLayout(layout)

    def login(self):
        user = self.input_user.text()
        pw = self.input_pass.text()
        self.controlador.procesar_login(user, pw)