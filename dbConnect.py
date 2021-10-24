import json
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

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
    return jsonlistaUsuarios


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
    return jsonlistaProveedores

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

    cursor.execute(
        """
            UPDATE Persona
            SET imagen_src = '%s', telefono_persona = '%s'
            WHERE id_persona = '%s'
        """ % (srcImagen, telefonoPersona, idPersona))

    conn.commit()
    conn.close()
    
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
            pro.cantidad_minima
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