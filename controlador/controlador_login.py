from vista.login_ui import LoginUI
from vista.menu_imagen_ui import MenuImagenUI
from vista.menu_senal_ui import MenuSenalUI
from modelo import base_datos

class ControladorLogin:
    def __init__(self):
        self.login_ui = LoginUI(self)
        self.login_ui.show()

    def procesar_login(self, usuario, contrasena):
        rol = base_datos.validar_usuario(usuario, contrasena)
        if rol == "imagen":
            self.login_ui.close()
            self.menu = MenuImagenUI()
            self.menu.show()
        elif rol == "senal":
            self.login_ui.close()
            self.menu = MenuSenalUI()
            self.menu.show()
        else:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(self.login_ui, "Error", "Usuario o contraseña incorrectos")

    