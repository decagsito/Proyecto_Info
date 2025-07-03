import sys
from PyQt5.QtWidgets import QApplication
from modelo import base_datos
from controlador.controlador_login import ControladorLogin

if __name__ == '__main__':
    base_datos.crear_tabla_usuarios()
    base_datos.crear_tabla_imagenes()
    # Puedes insertar usuarios para prueba aquí
    base_datos.insertar_usuario("julian", "1234", "imagen")
    base_datos.insertar_usuario("david", "5678", "senal")

    app = QApplication(sys.argv)
    controlador = ControladorLogin()
    sys.exit(app.exec_())