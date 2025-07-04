import sqlite3
from datetime import datetime

def conectar():
    return sqlite3.connect("usuarios.db")

def crear_tabla_usuarios():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE,
            contrasena TEXT,
            rol TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insertar_usuario(usuario, contrasena, rol):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO usuarios (usuario, contrasena, rol) VALUES (?, ?, ?)',
                       (usuario, contrasena, rol))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

def validar_usuario(usuario, contrasena):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT rol FROM usuarios WHERE usuario=? AND contrasena=?',
                   (usuario, contrasena))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None

def crear_tabla_imagenes():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS imagenes_medicas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT,
            ruta_dicom TEXT,
            ruta_nifti TEXT,
            fecha TEXT
        )
    ''')
    conn.commit()
    conn.close()

def registrar_conversion_dicom_a_nifti(ruta_dicom, ruta_nifti):
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO imagenes_medicas (tipo, ruta_dicom, ruta_nifti, fecha)
        VALUES (?, ?, ?, ?)
    ''', ('DICOM/NIfTI', ruta_dicom, ruta_nifti, fecha))
    conn.commit()
    conn.close()

def crear_tabla_archivos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS archivos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT,
            nombre_archivo TEXT,
            fecha TEXT,
            ruta TEXT
        )
    ''')
    conn.commit()
    conn.close()

def registrar_archivo(tipo, nombre_archivo, ruta):
    conn = conectar()
    cursor = conn.cursor()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO archivos (tipo, nombre_archivo, fecha, ruta)
        VALUES (?, ?, ?, ?)
    ''', (tipo, nombre_archivo, fecha, ruta))
    conn.commit()
    conn.close()

def obtener_dicom_nifti():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT tipo, ruta_dicom, ruta_nifti, fecha FROM imagenes_medicas")
    datos = cursor.fetchall()
    conn.close()
    return datos

def obtener_archivos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT tipo, nombre_archivo, ruta, fecha FROM archivos")
    datos = cursor.fetchall()
    conn.close()
    return datos