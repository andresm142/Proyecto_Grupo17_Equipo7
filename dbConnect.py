import sqlite3

def crearConexion():
    conn = sqlite3.connect(r'static/db/SaicMotor.db')
    return conn


