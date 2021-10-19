import sqlite3
import secrets

# Ruta relativa de conexión a la base de datos
database = r'static/db/SaicMotor.db'


def crearConexion():
    """ Crear e inicializar conexión a la base de datos.

    Este método crea e inicializa una conexión a la base de datos.

    Args: None
    """

    conn = sqlite3.connect(database)
    return conn


def validarUsuario(cuentaCorreo):
    """ Valida si una cuenta de correo existe en la base de datos.

    Este método recibe una cuenta de correo electrónico y valida si existe en la base de datos.

    Parameters

    cuentaCorreo -- Es la cuenta de correo que se validará si existe en la base de datos.
    """

    # Crear nuevamente la conexión a la base de datos. Por buenas prácticas, se debe cerrar
    # la conexión después de cada ejecución de un método/proceso.
    conn = crearConexion()
    cursor = conn.cursor()

    # Verificar si el correo existe en la base de datos.
    queryUser = cursor.execute(
        "SELECT email FROM Persona WHERE email = '%s'" % cuentaCorreo).fetchone()

    # Si queryUser trae datos, se toma el primer valor de la tupla.
    if queryUser is not None:
        queryUser = queryUser[0]

    # Si el correo existe, se envía un True como confirmación.
    if queryUser == cuentaCorreo:
        conn.close()
        return queryUser
    else:
        conn.close()
        return False


def validarContrasena(cuentaCorreo, password):
    """ Valida si la claves es correcta.

    Este método recibe una cuenta de correo electrónico y la contraseña, valida si la contraseña
    es correcta y está asociada al correo indicado.

    Parameters

    cuentaCorreo -- Es la cuenta de correo que se validará.

    password -- Es la contraseña que se validará.
    """

    if validarUsuario(cuentaCorreo) is not False:
        # Crear nuevamente la conexión a la base de datos. Por buenas prácticas, se debe cerrar
        # la conexión después de cada ejecución de un método/proceso.
        conn = crearConexion()
        cursor = conn.cursor()

        queryPass = cursor.execute(
            "SELECT usr.contrasena FROM Persona per, Usuario usr WHERE usr.id_persona = per.id_persona AND per.email = '%s'" % cuentaCorreo).fetchone()
    else:
        return False

    if queryPass[0] == password:
        conn.close()
        return True
    else:
        conn.close()
        return False


def validarTipoUsuario(cuentaCorreo):
    """ Valida el tipo de usuario (Usuario, Admin, Super-Admin).

    Este método recibe una cuenta de correo electrónico y valida el tipo o rol de usuario asignado.

    Parameters

    cuentaCorreo -- Es la cuenta de correo que se validará.
    """

    if validarUsuario(cuentaCorreo) is not False:
        # Crear nuevamente la conexión a la base de datos. Por buenas prácticas, se debe cerrar
        # la conexión después de cada ejecución de un método/proceso.
        conn = crearConexion()
        cursor = conn.cursor()

        queryUserType = cursor.execute(
        "SELECT rol.descripcion_rol FROM Persona per, Usuario usr, Rol rol WHERE usr.id_persona = per.id_persona AND rol.id_rol = usr.id_rol AND per.email = '%s'" % cuentaCorreo).fetchone()
        
        conn.close()
        return queryUserType[0]
    else:
        return False


def obtenerIDUsuario(cuentaCorreo):
    """ Obtener el id del usuario de la base de datos en base a un correo.

    Este método recibe una cuenta de correo electrónico y busca el id de usuario asociado en la tabla Usuario.

    Parameters

    cuentaCorreo -- Es la cuenta de correo que se validará.
    """

    if validarUsuario(cuentaCorreo) is not False:
        # Crear nuevamente la conexión a la base de datos. Por buenas prácticas, se debe cerrar
        # la conexión después de cada ejecución de un método/proceso.
        conn = crearConexion()
        cursor = conn.cursor()

        queryUserId = cursor.execute(
        "SELECT usr.id_usuario FROM Usuario usr, Persona per WHERE per.id_persona = usr.id_persona AND per.email = '%s'" % cuentaCorreo).fetchone()
        
        conn.close()
        return queryUserId[0]
    else:
        return False


def cambiarContraseña(idUsuario, password):
    """ Cambiar contraseña de acceso.

    Este método recibe una cuenta de correo electrónico a la cual le será asignada la respectiva contraseña.

    Parameters

    cuentaCorreo -- Es la cuenta de correo a la que le será realizado el cambio de clave.

    password -- Es la nueva contraseña que será asignada al usuario.
    """

    # Crear nuevamente la conexión a la base de datos. Por buenas prácticas, se debe cerrar
    # la conexión después de cada ejecución de un método/proceso.
    conn = crearConexion()
    cursor = conn.cursor()

    # Se actualiza la contraseña del usuario.
    queryUpdatePass = cursor.execute(
        """
        UPDATE Usuario
                SET contrasena = '%s'
                WHERE Usuario.id_persona = '%s';
        """ % (password, idUsuario))

    conn.commit()
    conn.close()


def cambiarEstatusUsuario(tipoEstatus, idUsuario):
    """ Cambiar el estatus de un usuario en la base de datos.

    Este método recibe un entero que indicará a la base de datos el estatus de usuario. El estatus de valor = 1 significa
    que el usuario está activo y no tiene cambio de claves pendiente. El valor de estatus = 0, significa que el usuario
    solicitó un cambio de contraseña, le fue enviado el correo para restablecerla pero aún no inicia sesión y cambia su clave.

    Parameters

    tipoEstatus -- 0 para usuarios pendientes de cambiar clave, 1 para usuarios sin problemas.
    """

    # Crear nuevamente la conexión a la base de datos. Por buenas prácticas, se debe cerrar
    # la conexión después de cada ejecución de un método/proceso.
    conn = crearConexion()
    cursor = conn.cursor()

    # Se actualiza el estatus del usuario.
    queryUpdateStatus = cursor.execute(
        """
        UPDATE Usuario
                SET estatus_usuario = '%s'
                WHERE Usuario.id_persona = '%s';
        """ % (tipoEstatus, idUsuario))

    conn.commit()
    conn.close()


def obtenerDatosUsuario(cuentaCorreo):
    """ Obtener los datos del usuario.

    Este método recibe una cuenta de correo electrónico y busca los datos del usuario asociados en las
    diferentes tablas, como datos personales, rol del usuario, la sede a la que pertenece, la ciudad, etc.
    """

    # Crear nuevamente la conexión a la base de datos. Por buenas prácticas, se debe cerrar
    # la conexión después de cada ejecución de un método/proceso.
    conn = crearConexion()
    cursor = conn.cursor()

    queryDatosUsuario = cursor.execute(
        """
            SELECT per.id_persona, per.nombre_persona, per.apellido_persona, per.telefono_persona, per.email, per.imagen_src,
                    usr.id_usuario, usr.estatus_usuario, rol.descripcion_rol, sede.nombre_sede, ciudad.nombre_ciudad, pais.nombre_pais
            
            FROM Persona per, Usuario usr, Rol rol, Sede sede, Ciudad ciudad, Pais pais
            
            WHERE usr.id_persona = per.id_persona AND rol.id_rol = usr.id_rol AND usr.id_sede = sede.id_sede
            AND sede.id_ciudad = ciudad.id_ciudad AND ciudad.id_pais = pais.id_pais
            AND per.email =  '%s'
        """ % cuentaCorreo)

    i = 0
    datosUsuario = {}
    datosDB = queryDatosUsuario.fetchone()
    nombreColumnas = [i[0] for i in cursor.description]

    for nombre in nombreColumnas:
        datosUsuario[nombre] = datosDB[i]
        i += 1
    
    conn.close()
    return datosUsuario


def recuperarContrasena(cuentaCorreo, idUsuario, password):
    """ Recuperar contraseña de acceso.

    Este método recibe una cuenta de correo electrónico a la cual le será asignada la respectiva contraseña.

    Parameters

    cuentaCorreo -- Es la cuenta de correo a la que le será realizado el cambio de clave.
    """

    # Se actualiza la contraseña del usuario.
    cambiarContraseña(idUsuario, password)

    # Se actualiza el estatus del usuario para forzar a cambiar la contraseña al iniciar sesión por primera vez.
    cambiarEstatusUsuario(0, idUsuario)
