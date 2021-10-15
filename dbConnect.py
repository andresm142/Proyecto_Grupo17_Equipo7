import sqlite3

database = r'static/db/SaicMotor.db'
conn = sqlite3.connect("")


def crearConexion():
    global conn
    conn = sqlite3.connect(database)


def validarUsuario(usuario, password):
    cursor = conn.cursor()

    queryUser = cursor.execute("SELECT email FROM Persona WHERE email = '%s'" % usuario).fetchone()
    queryPass = cursor.execute(
        "SELECT usr.contrasena FROM Persona per, Usuario usr WHERE usr.id_persona = per.id_persona AND per.email = '%s'" % usuario).fetchone()

    if queryUser is not None and queryPass is not None:
        queryUser = queryUser[0]
        queryPass = queryPass[0]

    if queryUser == usuario and queryPass == password:
        conn.close()
        return True
    else:
        conn.close()
        return False


def validarTipoUsuario(usuario):
    # Crear nuevamente la conexión a la base de datos. Cada ejecución de un método la cierra.
    crearConexion()
    cursor = conn.cursor()

    queryUser = cursor.execute("SELECT email FROM Persona WHERE email = '%s'" % usuario).fetchone()
    queryUserType = cursor.execute(
        "SELECT rol.descripcion_rol FROM Persona per, Usuario usr, Rol rol WHERE usr.id_persona = per.id_persona AND rol.id_rol = usr.id_rol AND per.email = '%s'" % usuario).fetchone()

    if queryUser is not None and queryUserType is not None:
        queryUser = queryUser[0]
        queryUserType = queryUserType[0]

    if queryUser == usuario:
        conn.close()
        return queryUserType
    else:
        conn.close()
        return ""
