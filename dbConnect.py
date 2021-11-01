import datetime
import json
import random
import sqlite3
import string
from flask.helpers import flash
from werkzeug.security import generate_password_hash, check_password_hash
import enviarEmail

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
            "SELECT usr.contrasena FROM Persona per, Usuario usr WHERE usr.id_persona = per.id_persona AND per.email = '%s'" % cuentaCorreo).fetchone()[0]
    else:
        return False
    
    if check_password_hash(queryPass, password):
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


def cambiarContrasena(idUsuario, password):
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


def buscarIdRol(rol):
    """ Buscar el id del rol de la base de datos.

    Este método recibe una descripción de rol y busca el id de rol asociado en la tabla Rol.

    Parameters

    rol -- Es la descripción del rol que se buscará.
    """

    # Crear nuevamente la conexión a la base de datos. Por buenas prácticas, se debe cerrar
    # la conexión después de cada ejecución de un método/proceso.
    conn = crearConexion()
    cursor = conn.cursor()

    queryRolId = cursor.execute(
        "SELECT id_rol FROM Rol WHERE descripcion_rol = '%s'" % rol).fetchone()

    conn.close()
    return queryRolId[0]


def comprobarEstatusUsuario(idUsuario):
    """ Comprobar el estatus del usuario.

    Este método recibe un id de usuario y busca el estatus de la persona asociada al usuario.

    Parameters

    idUsuario -- Es el id del usuario que se buscará.
    """

    # Crear nuevamente la conexión a la base de datos. Por buenas prácticas, se debe cerrar
    # la conexión después de cada ejecución de un método/proceso.
    conn = crearConexion()
    cursor = conn.cursor()

    queryEstatus = cursor.execute(
        "SELECT estatus_usuario FROM Usuario WHERE id_usuario = '%s'" % idUsuario).fetchone()

    conn.close()
    return queryEstatus[0]


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


def obtenerListaDeUsuarios():
    """ Obtener un listado de usuarios creado en la plataforma.

    Este método devuelve un listado de usuarios para ser mostrados en la página Usuarios.html.
    """

    # Crear nuevamente la conexión a la base de datos. Por buenas prácticas, se debe cerrar
    # la conexión después de cada ejecución de un método/proceso.
    conn = crearConexion()
    cursor = conn.cursor()

    queryDatosUsuarios = cursor.execute(
        """
            SELECT per.id_persona, per.nombre_persona, per.apellido_persona, Rol.descripcion_rol, per.email, per.imagen_src
            FROM Persona per,
                Rol,
                Usuario usr
            WHERE usr.id_rol = rol.id_rol
            AND per.id_persona = usr.id_persona
        """)
    

    nombreColumnas = [i[0] for i in cursor.description]
    datosUsuariosDB = queryDatosUsuarios.fetchall()

    jsonlistaUsuarios=[]
    for result in datosUsuariosDB:
        jsonlistaUsuarios.append(dict(zip(nombreColumnas,result)))
    
    conn.close()

    return jsonlistaUsuarios


def recuperarContrasena(cuentaCorreo, idUsuario, password):
    """ Recuperar contraseña de acceso.

    Este método recibe una cuenta de correo electrónico a la cual le será asignada la respectiva contraseña.

    Parameters

    cuentaCorreo -- Es la cuenta de correo a la que le será realizado el cambio de clave.
    """

    # Se actualiza la contraseña del usuario.
    cambiarContrasena(idUsuario, password)

    # Se actualiza el estatus del usuario para forzar a cambiar la contraseña al iniciar sesión por primera vez.
    cambiarEstatusUsuario(0, idUsuario)

def listaProductos():
    """ Obtener un listado de productos creados en la plataforma.

    Este método devuelve un listado de productos para ser mostrados en la página Productos.html.
    """

    # Crear nuevamente la conexión a la base de datos. Por buenas prácticas, se debe cerrar
    # la conexión después de cada ejecución de un método/proceso.
    conn = crearConexion()
    cursor = conn.cursor()

    queryDatosProductos = cursor.execute(
        """
            SELECT pro.id_producto,
                pro.nombre_producto,
                prove.id_proveedor,
                prove.nombre_proveedor,
                pro.descripcion_producto,
                pro.calificacion,
                pro.src_imagen,
                alm.cantidad_disponible
            FROM Producto pro, Almacen alm, Proveedor prove
            WHERE alm.id_producto = pro.id_producto AND alm.id_proveedor = prove.id_proveedor
            ORDER BY pro.fecha_creado DESC;
        """)

    nombreColumnas = [i[0] for i in cursor.description]
    datosUsuariosDB = queryDatosProductos.fetchall()

    jsonlistaProductos=[]
    for result in datosUsuariosDB:
        jsonlistaProductos.append(dict(zip(nombreColumnas,result)))
    
    conn.close()
    return jsonlistaProductos

def listaProveedores():
    """ Obtener un listado de proveedores creados en la plataforma.

    Este método devuelve un listado de proveedores para ser mostrados en la página Proveedores.html.
    """

    # Crear nuevamente la conexión a la base de datos. Por buenas prácticas, se debe cerrar
    # la conexión después de cada ejecución de un método/proceso.
    conn = crearConexion()
    cursor = conn.cursor()

    queryDatosProveedores = cursor.execute(
        """
            SELECT  pro.id_proveedor,
                    pro.nombre_proveedor,
                    pro.descripcion_proveedor,
                    pro.src_imagen
            FROM Proveedor pro
            ORDER BY pro.fecha_creado DESC
        """)

    nombreColumnas = [i[0] for i in cursor.description]
    datosProveedoresDB = queryDatosProveedores.fetchall()

    jsonlistaProveedores=[]
    for result in datosProveedoresDB:
        jsonlistaProveedores.append(dict(zip(nombreColumnas,result)))
    
    conn.close()

    return jsonlistaProveedores


def listaEmailUsuarios():
    """ Obtener un listado de correos electrónicos de los usuarios.

    Este método devuelve un listado de correos electrónicos de los usuarios para ser mostrados en la página
    listas para el envío de correo de productos pendientes de stock.
    """

    # Crear nuevamente la conexión a la base de datos. Por buenas prácticas, se debe cerrar
    # la conexión después de cada ejecución de un método/proceso.
    conn = crearConexion()
    cursor = conn.cursor()

    queryDatosUsuarios = cursor.execute(
        """
            SELECT per.email
            FROM Persona per,
                Usuario usr
            WHERE usr.id_persona = per.id_persona
        """)

    nombreColumnas = [i[0] for i in cursor.description]
    datosUsuariosDB = queryDatosUsuarios.fetchall()

    jsonlistaUsuarios=[]
    for result in datosUsuariosDB:
        jsonlistaUsuarios.append(dict(zip(nombreColumnas,result)))
    
    conn.close()

    return jsonlistaUsuarios



def autocompletarListaProductos():
    listaProducto = listaProductos()
    msj = ""
    for producto in listaProducto:
        msj += producto['nombre_producto'] + ","
    return msj


def autocompletarListaProveedores():
    listaProveedor = listaProveedores()

    msj = ""
    for proveedor in listaProveedor:
        msj += proveedor['nombre_proveedor'] + ","
    return msj

def autocompletarListaEmail():
    listaEmail = listaEmailUsuarios()

    msj = ""
    for email in listaEmail:
        msj += email['email'] + ","
    return msj


def buscarIdProveedor(nombreProveedor):
    """ Buscar un proveedor por su nombre.

    Este método busca un proveedor por su nombre y devuelve su id.
    """

    # Crear nuevamente la conexión a la base de datos. Por buenas prácticas, se debe cerrar
    # la conexión después de cada ejecución de un método/proceso.
    conn = crearConexion()
    cursor = conn.cursor()

    queryIdProveedor = cursor.execute(
        """
            SELECT id_proveedor
            FROM Proveedor
            WHERE nombre_proveedor = '%s'
        """ % (nombreProveedor))

    idProveedor = queryIdProveedor.fetchone()

    conn.close()

    return idProveedor[0]


def obtenerDatosUsuarioById(id):
    """ Obtener los datos del usuario por su id.

    Este método recibe un id y busca los datos del usuario asociados en las
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
            AND per.id_persona =  '%s'
        """ % id)

    i = 0
    datosUsuario = {}
    datosDB = queryDatosUsuario.fetchone()
    nombreColumnas = [i[0] for i in cursor.description]

    for nombre in nombreColumnas:
        datosUsuario[nombre] = datosDB[i]
        i += 1
    
    conn.close()
    return datosUsuario

def obtenerProveedorById(id):
    """ Obtener los datos del proveedor por su id.

    Este método recibe un id y busca los datos del proveedor asociados en las
    diferentes tablas.
    """

    # Crear nuevamente la conexión a la base de datos. Por buenas prácticas, se debe cerrar
    # la conexión después de cada ejecución de un método/proceso.
    conn = crearConexion()
    cursor = conn.cursor()

    queryDatosProveedor = cursor.execute(
        """
            SELECT  pro.id_proveedor,
                    pro.nombre_proveedor,
                    pro.descripcion_proveedor,
                    pro.src_imagen
            FROM Proveedor pro
            WHERE pro.id_proveedor = '%s'
        """ % id)

    i = 0
    datosProveedor = {}
    datosDB = queryDatosProveedor.fetchone()
    nombreColumnas = [i[0] for i in cursor.description]

    for nombre in nombreColumnas:
        datosProveedor[nombre] = datosDB[i]
        i += 1
    
    conn.close()
    return datosProveedor


def obtenerProductoPorID(idProveedor, idProducto):
    """ Obtener los datos del producto por su id.

    Este método recibe un id y busca los datos del producto asociados en las
    diferentes tablas.
    """

    # Crear nuevamente la conexión a la base de datos. Por buenas prácticas, se debe cerrar
    # la conexión después de cada ejecución de un método/proceso.
    conn = crearConexion()
    cursor = conn.cursor()

    queryDatosProducto = cursor.execute(
        """
            SELECT pro.id_producto,
                pro.nombre_producto,
                prove.nombre_proveedor,
                pro.descripcion_producto,
                pro.calificacion,
                pro.src_imagen,
                alm.cantidad_disponible,
                pro.cantidad_minima
            FROM Producto pro, Almacen alm, Proveedor prove
            WHERE alm.id_producto = pro.id_producto AND alm.id_proveedor = prove.id_proveedor AND pro.id_producto=alm.id_producto AND pro.id_producto='%s' AND alm.id_proveedor = '%s'
        """ % (idProducto, idProveedor))
   
    i = 0
    datosProducto = {}
    datosDB = queryDatosProducto.fetchone()
    nombreColumnas = [i[0] for i in cursor.description]

    for nombre in nombreColumnas:
        datosProducto[nombre] = datosDB[i]
        i += 1
    
    conn.close()   
        
    return datosProducto


def cambiarImagenProducto(srcProducto, idProducto):
    """ Cambiar la imagen del producto.

    Este método recibe una imagen y la cambia en la base de datos.
    """

    # Crear nuevamente la conexión a la base de datos. Por buenas prácticas, se debe cerrar
    # la conexión después de cada ejecución de un método/proceso.
    conn = crearConexion()
    cursor = conn.cursor()

    cursor.execute(
        """
            UPDATE Producto
            SET src_imagen = '%s'
            WHERE id_producto = '%s'
        """ % (srcProducto, idProducto))

    conn.commit()
    conn.close()


def editarConfiguracionUsuario(srcImagen, idPersona, telefonoPersona):
    """ Editar la configuración del usuario.

    Este método recibe una imagen, un id y un telefono y los cambia en la base de datos.
    """

    # Crear nuevamente la conexión a la base de datos. Por buenas prácticas, se debe cerrar
    # la conexión después de cada ejecución de un método/proceso.
    conn = crearConexion()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
                UPDATE Persona
                SET imagen_src = '%s', telefono_persona = '%s'
                WHERE id_persona = '%s'
            """ % (srcImagen, telefonoPersona, idPersona))

        conn.commit()
        conn.close()

    except sqlite3.Error as er:
        if er.args[0] == 'UNIQUE constraint failed: Persona.email':
            conn.close()
            return False, flash('El correo ya está registrado.')
        elif er.args[0] == 'UNIQUE constraint failed: Persona.telefono_persona':
            conn.close()
            return False, flash('El teléfono ya está registrado.')
 
    return True, flash('Datos actualizados correctamente.')
   
def editarConfiguracionUsuarioSinImagen(id_persona,telefono_persona):
    """ Editar la configuración del usuario.

    Este método recibe un id y un telefono y los cambia en la base de datos.
    """

    # Crear nuevamente la conexión a la base de datos. Por buenas prácticas, se debe cerrar
    # la conexión después de cada ejecución de un método/proceso.
    conn = crearConexion()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
                UPDATE Persona
                SET telefono_persona = '%s'
                WHERE id_persona = '%s'
            """ % (telefono_persona, id_persona))
        conn.commit()
        conn.close()
    except sqlite3.Error as er:
        if er.args[0] == 'UNIQUE constraint failed: Persona.email':
            conn.close()
            return False, flash('El correo ya está registrado.')
        elif er.args[0] == 'UNIQUE constraint failed: Persona.telefono_persona':
            conn.close()
            return False, flash('El teléfono ya está registrado.')
    return True, flash('Datos actualizados correctamente.')
 
def buscarPorProducto(texto):
    """ Editar la configuración del usuario.

    Este método recibe una imagen, un id y un telefono y los cambia en la base de datos.
    """

    # Crear nuevamente la conexión a la base de datos. Por buenas prácticas, se debe cerrar
    # la conexión después de cada ejecución de un método/proceso.
    conn = crearConexion()
    cursor = conn.cursor()

    queryDatosProducto = cursor.execute(
    """
        SELECT pro.id_producto,
            pro.nombre_producto,
            prove.nombre_proveedor,
            pro.descripcion_producto,
            pro.calificacion,
            pro.src_imagen,
            alm.cantidad_disponible,
            pro.cantidad_minima,
            prove.id_proveedor
        FROM Producto pro, Almacen alm, Proveedor prove
        WHERE alm.id_producto = pro.id_producto AND alm.id_proveedor = prove.id_proveedor AND pro.id_producto=alm.id_producto AND pro.nombre_producto LIKE '%s'
    """ % ('%'+texto+'%'))
    
    nombreColumnas = [i[0] for i in cursor.description]
    datosProductosDB = queryDatosProducto.fetchall()

    jsonlistaProductos=[]
    for result in datosProductosDB:
        jsonlistaProductos.append(dict(zip(nombreColumnas,result)))
    
    conn.close()
    return jsonlistaProductos

def buscarPorProveedor(texto):
    """ Editar la configuración del usuario.

    Este método recibe una imagen, un id y un telefono y los cambia en la base de datos.
    """

    # Crear nuevamente la conexión a la base de datos. Por buenas prácticas, se debe cerrar
    # la conexión después de cada ejecución de un método/proceso.
    conn = crearConexion()
    cursor = conn.cursor()

    queryDatosProveedor = cursor.execute(
    """
            SELECT  pro.id_proveedor,
                    pro.nombre_proveedor,
                    pro.descripcion_proveedor,
                    pro.src_imagen
            FROM Proveedor pro
            WHERE pro.nombre_proveedor LIKE '%s'
        """ % ('%'+texto+'%'))
    
    
    nombreColumnas = [i[0] for i in cursor.description]
    datosProveedorDB = queryDatosProveedor.fetchall()

    jsonlistaProveedor=[]
    for result in datosProveedorDB:
        jsonlistaProveedor.append(dict(zip(nombreColumnas,result)))
    
    conn.close()
    return jsonlistaProveedor


def crearContrasena():
    """ Crear una contraseña aleatoria.

    Este método crea una contraseña aleatoria.
    """
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))


def insertarPersona(nombre, apellido, telefono, email, imagen_src, rolUsuario):
    """ Insertar una persona en la base de datos.

    Este método recibe los datos de una persona y los inserta en la base de datos.
    """

    # Crear nuevamente la conexión a la base de datos. Por buenas prácticas, se debe cerrar
    # la conexión después de cada ejecución de un método/proceso.
    conn = crearConexion()
    cursor = conn.cursor()
    try:       
        cursor.execute(
            """
                INSERT INTO Persona (nombre_persona, apellido_persona, telefono_persona, email, imagen_src)
                VALUES ('%s', '%s', '%s', '%s', '%s')
            """ % (nombre, apellido, telefono, email, imagen_src))

        conn.commit()
        conn.close()
    except sqlite3.Error as er:
        if er.args[0] == 'UNIQUE constraint failed: Persona.email':
            conn.close()
            return False, flash('El correo ya está registrado.')
        elif er.args[0] == 'UNIQUE constraint failed: Persona.telefono_persona':
            conn.close()
            return False, flash('El teléfono ya está registrado.')
        
    idPersona = cursor.lastrowid
    idRol = buscarIdRol(rolUsuario)
    password = crearContrasena()
    passwordHash = generate_password_hash(password)

    insertarUsuario(idPersona, idRol, passwordHash)

    idUsuario = obtenerIDUsuario(email)
    enviarEmailCreacionCuenta(email, nombre + " " + apellido, idUsuario, password)
    return True


def insertarUsuario(idPersona, idRol, contrasena):
    """ Insertar un usuario en la base de datos.

    Este método recibe los datos de un usuario y los inserta en la base de datos.
    """

    # Crear nuevamente la conexión a la base de datos. Por buenas prácticas, se debe cerrar
    # la conexión después de cada ejecución de un método/proceso.
    conn = crearConexion()
    cursor = conn.cursor()

    cursor.execute(
        """
            INSERT INTO Usuario (contrasena, estatus_usuario, id_persona, id_rol, id_sede)
            VALUES ('%s', 0, '%s', '%s', 1)
        """ % (contrasena, idPersona, idRol))

    conn.commit()
    conn.close()

def enviarEmailCreacionCuenta(email, nombreApellido, idUsuario, contrasena):
    datosEmail = enviarEmail.emailCrearUsuario(email, nombreApellido, idUsuario, contrasena)
    response = enviarEmail.enviarCorreo(datosEmail)


def insertarProveedor(nombreProveedor, descripcionProveedor, srcImagen):
    """ Insertar un proveedor en la base de datos.

    Este método recibe una imagen, un id y un telefono y los cambia en la base de datos.
    """

    # Crear nuevamente la conexión a la base de datos. Por buenas prácticas, se debe cerrar
    # la conexión después de cada ejecución de un método/proceso.
    conn = crearConexion()
    cursor = conn.cursor()
    fechaHora = datetime.datetime.now()

    cursor.execute(
        """
            INSERT INTO Proveedor (nombre_proveedor, descripcion_proveedor, src_imagen, fecha_creado, id_empresa)
            VALUES ('%s', '%s', '%s', '%s', '%s')
        """ % (nombreProveedor, descripcionProveedor, srcImagen, fechaHora, 1))

    conn.commit()
    conn.close()


def insertarProducto(nombreProducto, descripcionProducto, calificacion, srcImagen, cantidadMinima, cantidadDisponible, nombreProveedor):
    """ Insertar un producto en la base de datos.

    Este método recibe una imagen, un id y un telefono y los cambia en la base de datos.
    """

    # Crear nuevamente la conexión a la base de datos. Por buenas prácticas, se debe cerrar
    # la conexión después de cada ejecución de un método/proceso.
    conn = crearConexion()
    cursor = conn.cursor()

    fechaHora = datetime.datetime.now()

    cursor.execute(
        """
            INSERT INTO Producto (nombre_producto, descripcion_producto, calificacion, src_imagen, fecha_creado, id_empresa, cantidad_minima)
            VALUES ('%s', '%s', %s, '%s', '%s', %s, %s)
        """ % (nombreProducto, descripcionProducto, calificacion, srcImagen, fechaHora, 1, cantidadMinima))

    conn.commit()
    conn.close()

    idProducto = cursor.lastrowid
    idProveedor = buscarIdProveedor(nombreProveedor)
    insertarRegistroAlmacen(idProducto, idProveedor, cantidadDisponible)


def insertarRegistroAlmacen(idProducto, idProveedor, cantidadDisponible):
    """ Insertar un registro de almacén en la base de datos.

    Este método recibe una imagen, un id y un telefono y los cambia en la base de datos.
    """

    # Crear nuevamente la conexión a la base de datos. Por buenas prácticas, se debe cerrar
    # la conexión después de cada ejecución de un método/proceso.
    conn = crearConexion()
    cursor = conn.cursor()


    cursor.execute(
        """
            INSERT INTO Almacen (id_bodega, id_producto, id_proveedor, cantidad_disponible)
            VALUES (%s, %s, %s, %s)
        """ % (1, idProducto, idProveedor, cantidadDisponible))

    conn.commit()
    conn.close()
    
def obtnerProductosMinimosDiponible():
    """ Obtener los productos con cantidad mínima disponible.

    Este método obtiene los productos con cantidad mínima disponible.
    """

    # Crear nuevamente la conexión a la base de datos. Por buenas prácticas, se debe cerrar
    # la conexión después de cada ejecución de un método/proceso.
    conn = crearConexion()
    cursor = conn.cursor()

    queryDatosProductos=cursor.execute(
        """
            SELECT  pro.nombre_producto,
                        pro.id_producto,
                        prov.id_proveedor,
                        pro.cantidad_minima,
                        prov.nombre_proveedor,
                        alm.cantidad_disponible
                    FROM Producto pro, Almacen alm, Proveedor prov
                    WHERE pro.cantidad_minima > alm.cantidad_disponible AND alm.id_producto=pro.id_producto AND alm.id_proveedor=prov.id_proveedor
        """
    )


    nombreColumnas = [i[0] for i in cursor.description]
    datosProductos = queryDatosProductos.fetchall()

    jsonProductos = []

    for result in datosProductos:
        jsonProductos.append(dict(zip(nombreColumnas,result)))

    conn.close()
    return jsonProductos

def actualizarProducto(idProducto, nombreProducto, descripcionProducto, calificacion, srcImagen, cantidadMinima, cantidadDisponible, nombreProveedor):
    """ Actualizar un producto en la base de datos.

    Este método recibe una imagen, un id y un telefono y los cambia en la base de datos.
    """

    # Crear nuevamente la conexión a la base de datos. Por buenas prácticas, se debe cerrar
    # la conexión después de cada ejecución de un método/proceso.
    conn = crearConexion()
    cursor = conn.cursor()

    cursor.execute(
        """
            UPDATE Producto
            SET nombre_producto = '%s',
                descripcion_producto = '%s',
                calificacion = %s,
                src_imagen = '%s',
                cantidad_minima = %s
            WHERE id_producto = %s
        """ % (nombreProducto, descripcionProducto, calificacion, srcImagen, cantidadMinima, idProducto))

    conn.commit()
    conn.close()

    idProveedor = buscarIdProveedor(nombreProveedor)
    actualizarRegistroAlmacen(idProducto, idProveedor, cantidadDisponible)


def actualizarRegistroAlmacen(idProducto, idProveedor, cantidadDisponible):
    """ Actualizar un registro de almacén en la base de datos.

    Este método recibe una imagen, un id y un telefono y los cambia en la base de datos.
    """

    # Crear nuevamente la conexión a la base de datos. Por buenas prácticas, se debe cerrar
    # la conexión después de cada ejecución de un método/proceso.
    conn = crearConexion()
    cursor = conn.cursor()

    cursor.execute(
        """
            UPDATE Almacen
            SET cantidad_disponible = %s
            WHERE id_producto = %s AND id_proveedor = %s
        """ % (cantidadDisponible, idProducto, idProveedor))

    conn.commit()
    conn.close()


def obtenerImagenProducto(idProducto):
    """ Obtener la imagen de un producto.

    Este método recibe un id y devuelve la imagen correspondiente.
    """

    # Crear nuevamente la conexión a la base de datos. Por buenas prácticas, se debe cerrar
    # la conexión después de cada ejecución de un método/proceso.
    conn = crearConexion()
    cursor = conn.cursor()

    cursor.execute(
        """
            SELECT src_imagen
            FROM Producto
            WHERE id_producto = %s
        """ % (idProducto))

    imagen = cursor.fetchone()

    conn.close()

    return imagen[0]

def eliminarRegistroAlmacen(idProducto, idProveedor):
    """ Eliminar un registro de almacén en la base de datos.

    Este método recibe el id de producto y un id de proveedor para eliminar su registro en la tabla Almacen.
    """

    # Crear nuevamente la conexión a la base de datos. Por buenas prácticas, se debe cerrar
    # la conexión después de cada ejecución de un método/proceso.
    conn = crearConexion()
    cursor = conn.cursor()

    cursor.execute(
        """
            DELETE FROM Almacen
            WHERE id_producto = %s AND id_proveedor = %s
        """ % (idProducto, idProveedor))

    conn.commit()
    conn.close()


def actualizarProveedor(idProveedor, nombreProveedor, descripcionProveedor, src_imagen):
    """ Actualizar un proveedor en la base de datos.

    Este método recibe los datos de un proveedor y actualiza la información en la base de datos.
    """

    # Crear nuevamente la conexión a la base de datos. Por buenas prácticas, se debe cerrar
    # la conexión después de cada ejecución de un método/proceso.
    conn = crearConexion()
    cursor = conn.cursor()

    cursor.execute(
        """
            UPDATE Proveedor
            SET nombre_proveedor = '%s',
                descripcion_proveedor = '%s',
                src_imagen = '%s'
            WHERE id_proveedor = %s
        """ % (nombreProveedor, descripcionProveedor, src_imagen, idProveedor))

    conn.commit()
    conn.close()


def obtenerImagenProveedor(idProveedor):
    """ Obtener la imagen de un proveedor.

    Este método recibe un id y devuelve la imagen correspondiente.
    """

    # Crear nuevamente la conexión a la base de datos. Por buenas prácticas, se debe cerrar
    # la conexión después de cada ejecución de un método/proceso.
    conn = crearConexion()
    cursor = conn.cursor()

    cursor.execute(
        """
            SELECT src_imagen
            FROM Proveedor
            WHERE id_proveedor = %s
        """ % (idProveedor))

    imagen = cursor.fetchone()

    conn.close()

    return imagen[0]


def eliminarProveedor(idProveedor):
    """ Eliminar un proveedor en la base de datos.

    Este método recibe el id de proveedor y lo elimina de la base de datos.
    """

    # Crear nuevamente la conexión a la base de datos. Por buenas prácticas, se debe cerrar
    # la conexión después de cada ejecución de un método/proceso.
    conn = crearConexion()
    cursor = conn.cursor()

    cursor.execute(
        """
            DELETE FROM Proveedor
            WHERE id_proveedor = %s
        """ % (idProveedor))

    conn.commit()
    conn.close()


def borrarRegistrosProveedorTdAlmacen(idProveedor):
    """ Borrar todos los registros de un proveedor en la tabla Almacen.

    Este método recibe el id de proveedor y lo elimina de la tabla Almacen.
    """

    # Crear nuevamente la conexión a la base de datos. Por buenas prácticas, se debe cerrar
    # la conexión después de cada ejecución de un método/proceso.
    conn = crearConexion()
    cursor = conn.cursor()

    cursor.execute(
        """
            DELETE FROM Almacen
            WHERE id_proveedor = %s
        """ % (idProveedor))

    conn.commit()
    conn.close()

    eliminarProveedor(idProveedor)


def actualizarPersona(idPersona, nombrePersona, apellidoPersona, telefono, email, src_imagen):
    """ Actualizar una persona en la base de datos.

    Este método recibe los datos de una persona y actualiza la información en la base de datos.
    """

    # Crear nuevamente la conexión a la base de datos. Por buenas prácticas, se debe cerrar
    # la conexión después de cada ejecución de un método/proceso.
    conn = crearConexion()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
                UPDATE Persona
                SET nombre_persona = '%s',
                    apellido_persona = '%s',
                    telefono_persona = '%s',
                    email = '%s',
                    imagen_src = '%s'
                WHERE id_persona = %s
            """ % (nombrePersona, apellidoPersona, telefono, email, src_imagen, idPersona))

        conn.commit()
        conn.close()
    except sqlite3.Error as er:
        if er.args[0] == 'UNIQUE constraint failed: Persona.email':
            conn.close()
            return False, flash('El correo ya está registrado.')
        elif er.args[0] == 'UNIQUE constraint failed: Persona.telefono_persona':
            conn.close()
            return False, flash('El teléfono ya está registrado.')

def actualizarRolUsuario(idUsuario, idRol):
    """ Actualizar un rol de usuario en la base de datos.

    Este método recibe los datos de una persona y actualiza la información en la base de datos.
    """

    # Crear nuevamente la conexión a la base de datos. Por buenas prácticas, se debe cerrar
    # la conexión después de cada ejecución de un método/proceso.
    conn = crearConexion()
    cursor = conn.cursor()

    cursor.execute(
        """
            UPDATE Usuario
            SET id_rol = %s
            WHERE id_usuario = %s
        """ % (idRol, idUsuario))

    conn.commit()
    conn.close()


def obtenerImagenPersona(idPersona):
    """ Obtener la imagen de una persona.

    Este método recibe un id y devuelve la imagen correspondiente.
    """

    # Crear nuevamente la conexión a la base de datos. Por buenas prácticas, se debe cerrar
    # la conexión después de cada ejecución de un método/proceso.
    conn = crearConexion()
    cursor = conn.cursor()

    cursor.execute(
        """
            SELECT imagen_src
            FROM Persona
            WHERE id_persona = %s
        """ % (idPersona))

    imagen = cursor.fetchone()

    conn.close()

    return imagen[0]


def obtenerIDUsuarioDesdePersona(idPersona):
    """ Obtener el id de un usuario.

    Este método recibe un id de persona y devuelve el id de usuario correspondiente.
    """

    # Crear nuevamente la conexión a la base de datos. Por buenas prácticas, se debe cerrar
    # la conexión después de cada ejecución de un método/proceso.
    conn = crearConexion()
    cursor = conn.cursor()

    cursor.execute(
        """
            SELECT id_usuario
            FROM Usuario
            WHERE id_persona = %s
        """ % (idPersona))

    idUsuario = cursor.fetchone()

    conn.close()

    return idUsuario[0]


def eliminarUsuario(idUsuario, idPersona):
    """ Eliminar un usuario en la base de datos.

    Este método recibe el id de usuario y lo elimina de la base de datos.
    """

    # Crear nuevamente la conexión a la base de datos. Por buenas prácticas, se debe cerrar
    # la conexión después de cada ejecución de un método/proceso.
    conn = crearConexion()
    cursor = conn.cursor()

    cursor.execute(
        """
            DELETE FROM Usuario
            WHERE id_usuario = %s
        """ % (idUsuario))

    conn.commit()
    conn.close()

    eliminarPersona(idPersona)


def eliminarPersona(idPersona):
    """ Eliminar una persona en la base de datos.

    Este método recibe el id de persona y lo elimina de la base de datos.
    """

    # Crear nuevamente la conexión a la base de datos. Por buenas prácticas, se debe cerrar
    # la conexión después de cada ejecución de un método/proceso.
    conn = crearConexion()
    cursor = conn.cursor()

    cursor.execute(
        """
            DELETE FROM Persona
            WHERE id_persona = %s
        """ % (idPersona))

    conn.commit()
    conn.close()
    
def productosDisponibles():
    """ Obtener los productos disponibles.

    Este método recibe una cantidad y devuelve los productos disponibles.
    """

    # Crear nuevamente la conexión a la base de datos. Por buenas prácticas, se debe cerrar
    # la conexión después de cada ejecución de un método/proceso.
    conn = crearConexion()
    cursor = conn.cursor()

    queryDatosProductos=cursor.execute(
        """
            SELECT pro.id_producto,
                pro.nombre_producto,
                prove.id_proveedor,
                prove.nombre_proveedor,
                pro.descripcion_producto,
                pro.calificacion,
                pro.src_imagen,
                alm.cantidad_disponible
            FROM Producto pro, Almacen alm, Proveedor prove
            WHERE alm.id_producto = pro.id_producto AND alm.id_proveedor = prove.id_proveedor AND alm.cantidad_disponible > 0
            ORDER BY pro.fecha_creado DESC;
        """ )

   
    nombreColumnas = [i[0] for i in cursor.description]
    datosUsuariosDB = queryDatosProductos.fetchall()

    jsonlistaProductos=[]
    for result in datosUsuariosDB:
        jsonlistaProductos.append(dict(zip(nombreColumnas,result)))
    
    conn.close()
    return jsonlistaProductos
    
def productosNoDisponibles():
    """ Obtener los productos no disponibles.

    Este método recibe una cantidad y devuelve los productos no disponibles.
    """

    # Crear nuevamente la conexión a la base de datos. Por buenas prácticas, se debe cerrar
    # la conexión después de cada ejecución de un método/proceso.
    conn = crearConexion()
    cursor = conn.cursor()

    queryDatosProductos=cursor.execute(
        """
            SELECT pro.id_producto,
                pro.nombre_producto,
                prove.id_proveedor,
                prove.nombre_proveedor,
                pro.descripcion_producto,
                pro.calificacion,
                pro.src_imagen,
                alm.cantidad_disponible
            FROM Producto pro, Almacen alm, Proveedor prove
            WHERE alm.id_producto = pro.id_producto AND alm.id_proveedor = prove.id_proveedor AND alm.cantidad_disponible = 0
            ORDER BY pro.fecha_creado DESC;
        """ )

   
    nombreColumnas = [i[0] for i in cursor.description]
    datosUsuariosDB = queryDatosProductos.fetchall()

    jsonlistaProductos=[]
    for result in datosUsuariosDB:
        jsonlistaProductos.append(dict(zip(nombreColumnas,result)))
    
    conn.close()
    return jsonlistaProductos