from PyQt5.QtWidgets import QApplication
from modelo import base_datos
from controlador.controlador_login import ControladorLogin
from modelo import base_datos

if __name__ == '__main__':
    base_datos.crear_tabla_usuarios()
    base_datos.crear_tabla_imagenes()
    base_datos.crear_tabla_archivos()

    # Puedes insertar usuarios para prueba aquí
    base_datos.insertar_usuario("julian", "1234", "imagen")
    base_datos.insertar_usuario("david", "5678", "senal")

    app = QApplication([])

    # Estilo global
    with open("vista/estilos.qss", "r") as f:
        app.setStyleSheet(f.read())
    login = ControladorLogin()
    app.exec_()