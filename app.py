import re
import secrets, os
import dbConnect
from flask import Flask, jsonify, render_template, request, session, redirect, flash
from flask_session import Session
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash

import enviarEmail

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(20)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['UPLOAD_FOLDER'] = './static/images/upload'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
Session(app)

# Instanciar módulo de conexión a la base de datos
conn = dbConnect

@app.route('/')
def login():
    if not session.get("username"):
        return render_template('Login.html')
    else:
        return redirect("/Home")


@app.route('/Index', methods=['GET', 'POST'])
def Index():
    if conn.validarContrasena(request.form["email"], request.form["password"]) is not False:

        # Verificar si el usuario solicitó recuperación de contraseña o es primera vez que inicia sesión
        if conn.comprobarEstatusUsuario(conn.obtenerIDUsuario(request.form["email"])) == 0:
            flash("Bienvenido a la aplicación, por favor cambia tu contraseña", "success")
            return render_template('CambiarContrasena.html', email=request.form["email"])
        else:
            session["username"] = request.form["email"]
            session["userType"] = conn.validarTipoUsuario(request.form["email"])
            datosusuarios=conn.obtenerDatosUsuario(request.form["email"])
            
            session["usuario"] = (datosusuarios['id_persona'],datosusuarios['nombre_persona'],datosusuarios['apellido_persona'],
                                datosusuarios['imagen_src']) 
            consultaProductos=conn.listaProductos()
            consultaProveedor=conn.listaProveedores()
            session['autocompletarProductos'] = conn.autocompletarListaProductos()
            session['autoCompletarProveedores'] = conn.autocompletarListaProveedores()
            
            return render_template('Index.html', userType=session["userType"],usuario=session["usuario"],consultaProductos=consultaProductos,
                                consultaProveedor=consultaProveedor,autocompletarProductos=session['autocompletarProductos'], 
                                autoCompletarProveedores=session['autoCompletarProveedores'])
    else:
        session["username"] = None
        flash("Correo o contraseña incorrectos")
        return redirect('/')


@app.route('/Home')
def Home():
    if not session.get("username"):
        return redirect("/")
    else:
        # Consulta para el index, aqui se realizaran dos consultas, Productos y proveedores.
        # La consulta productos retorna: 'nombre producto', 'Proveedor', 'disponibles', 'imagen_src','fecha_creado
        # La consulta proveedores retorna: 'nombre proveedor', 'imagen_src','fecha_creado'
        # Cada consulta se guarda en una variable distinta
        consultaProductos=conn.listaProductos()
        consultaProveedor=conn.listaProveedores()


        # return render_template('Index.html', userType=session["userType"],consultaProductos=consultaProductos,consultaProveedor=consultaProveedor)
        return render_template('Index.html', userType=session["userType"],usuario=session["usuario"],consultaProductos=consultaProductos,
                               consultaProveedor=consultaProveedor, autocompletarProductos=session['autocompletarProductos'], 
                               autoCompletarProveedores=session['autoCompletarProveedores'])


@app.route('/Productos', methods=['POST', 'GET'])
def Productos():
    if not session.get("username"):
        return redirect("/")
    else:
        # Consulta para productos retorna:(id,nombre_producto,proveedor,disponibles,descripcion,calificacion,imagen_src)
        lista=conn.listaProductos()
        session['autocompletarProductos'] = conn.autocompletarListaProductos()
        session['autoCompletarProveedores'] = conn.autocompletarListaProveedores()
        return render_template('Productos.html',lista=lista)

@app.route('/Listas', methods=['POST', 'GET'])
def Listas():
    if not session.get("username"):
        return redirect("/")
    else:
        lista=conn.obtnerProductosMinimosDiponible()
        # lista=""
        return render_template('Listas.html',lista=lista)


@app.route('/Configuracion', methods=['POST', 'GET'])
def Configuracion():
    if not session.get("username"):
        return redirect("/")
    else:
        if request.method == 'POST':
            
            datosusuarios=conn.obtenerDatosUsuarioById(request.form["id-user"])
            if(datosusuarios['descripcion_rol']=="admin"):
                datosusuarios['descripcion_rol']="Administrador"
            elif(datosusuarios['descripcion_rol']=="superAdmin"):
                datosusuarios['descripcion_rol']="Super administrador"
            else:
                datosusuarios['descripcion_rol']="Usuario";
                    
            return render_template('User.html',datosusuarios=datosusuarios)


@app.route('/Proveedores', methods=['POST', 'GET'])
def Proveedores():
    if not session.get("username"):
        return redirect("/")
    else:
        # Consulta para productos retorna:(id,nombre_proveedor,descripcion,imagen_src)
        lista=conn.listaProveedores()
        session['autocompletarProductos'] = conn.autocompletarListaProductos()
        session['autoCompletarProveedores'] = conn.autocompletarListaProveedores()
        return render_template('Proveedores.html',lista=lista)


@app.route('/Usuarios', methods=['POST', 'GET'])
def Usuarios():
    if not session.get("username"):
        return redirect("/")
    else:
        
        if session.get("userType")=='admin' or session.get("userType")=='superAdmin':
            ListaUsuarios = conn.obtenerListaDeUsuarios()
            
            for x in range(len(ListaUsuarios)):
                if(ListaUsuarios[x]['descripcion_rol']=="admin"):
                    ListaUsuarios[x]['descripcion_rol']="Administrador"
                elif(ListaUsuarios[x]['descripcion_rol']=="superAdmin"):
                    ListaUsuarios[x]['descripcion_rol']="Super administrador"
                else:
                    ListaUsuarios[x]['descripcion_rol']="Usuario";
                
            return render_template('Usuarios.html',ListaUsuarios=ListaUsuarios)
        else:
            return render_template('AccessDenied.html')

@app.route('/Logout', methods=['POST', 'GET'])
def Logout():
    session.pop('username', None)
    flash(" ")
    return redirect('/')


@app.route('/Editarproducto', methods=['POST', 'GET'])
def Editarproducto():
    if not session.get("username"):
        return redirect("/")
    else:
        
        if request.method == 'POST':
            
            
            if request.form['submit_button'] == 'editar':
                idProducto=request.form['id']
                idproveedor=request.form['idproveedor']
                # Aqui se recibe el id del producto para su busqueda en la base de datos, esta retorna los datos
                # del producto
                datosProducto = conn.obtenerProductoPorID(idproveedor, idProducto)
                proveedores=conn.listaProveedores()
                
                return render_template('EditarProducto.html',datosProducto=datosProducto,proveedores=proveedores)
            
            elif request.form['submit_button'] == 'eliminar':
                
                # consulta para eliminar producto
                conn.eliminarRegistroAlmacen(request.form['id'], request.form['idproveedor'])
                flash("Prodcuto eliminado correctamente")
                return redirect('/Productos')
                
            elif request.form['submit_button']=='Añadir +':
                # Formulario en blanco para añadir producto
                
                return redirect('/AnadirProductos')
                
            elif request.form['submit_button'] == 'Disponible':
                
                textoBuscar='productos'
                buscarPor='Disponibles'
                #Consulta para Disponibles. 
                resultadobusqueda=conn.productosDisponibles()        
                                             
                
                return render_template('Search.html',textoBuscar=textoBuscar,buscarPor=buscarPor,
                                       resultadobusqueda=resultadobusqueda)
                
                
            elif request.form['submit_button'] == 'No Disponible':
                textoBuscar='productos'
                buscarPor='No Disponibles'
                # Consulta para No disponible, se considera no disponible cuando la cantiada de productos es 0
                resultadobusqueda=conn.productosNoDisponibles()
                                         
                return render_template('Search.html',textoBuscar=textoBuscar,buscarPor=buscarPor,
                                       resultadobusqueda=resultadobusqueda)

@app.route('/AnadirProductos', methods=['POST', 'GET'])
def AnadirProductos():
    proveedores=conn.listaProveedores()               
    datosProducto={'id_producto':'0','id_proveedor':'','nombre_proveedor': 'Proveedor','calificacion':1,'src_imagen':'/static/images/Producto.jpg'}
    return render_template('AnadirProducto.html',datosProducto=datosProducto,proveedores=proveedores)
 
@app.route('/AdminUser', methods=['POST', 'GET'])
def AdminUser():
    if not session.get("username"):
        return redirect("/")
    else:
        if request.method == 'POST':
            
            if request.form.get('submit_button') == 'editar':
                
                # Aqui se recibe el id del usuario para su busqueda en la base de datos, esta retorna los datos
                # del usuario
                datosusuarios=conn.obtenerDatosUsuarioById(request.form["id"])
                
                if(datosusuarios['descripcion_rol']=="admin"):
                    datosusuarios['descripcion_rol']="Administrador"
                elif(datosusuarios['descripcion_rol']=="superAdmin"):
                    datosusuarios['descripcion_rol']="Super administrador"
                else:
                    datosusuarios['descripcion_rol']="Usuario";
                
                
                return render_template('AdminUser.html',datosusuarios=datosusuarios)
            
            elif request.form.get('submit_button') == 'eliminar':
                # Consulta para eliminar usuarios
                # consulta para obtner el tipo de usuario del que se quiere borrar
                datosusuarios=conn.obtenerDatosUsuarioById(request.form["id"])
                tipoUSuario=datosusuarios['descripcion_rol']
                if session['userType']=='admin':
                   
                    if tipoUSuario=="usuario":
                        conn.eliminarUsuario(conn.obtenerIDUsuarioDesdePersona(request.form["id"]), request.form["id"])        
                        flash("Usuario eliminado correctamente")
                    else: 
                        flash("No posees los permisos para borrar un usuario de tipo administrador y super administrador")
                else:
                    if session['userType']=='superAdmin':
                        if tipoUSuario=="usuario" or tipoUSuario=="admin":
                            # Puede borrar un usuario de tipo usuario y administrador, pero no super administrador
                            conn.eliminarUsuario(conn.obtenerIDUsuarioDesdePersona(request.form["id"]), request.form["id"])
                            flash("Usuario eliminado correctamente")
                        else:
                            flash("No se puede borrar un usuario de tipo Super administrador")
                        # conn.eliminarUsuario(conn.obtenerIDUsuarioDesdePersona(request.form["id"]), request.form["id"])
                        
                return redirect('/Usuarios')
            elif request.form.get('submit_button')=='Añadir usuario +':
                                          
                datosusuarios={'id_persona': 0, 'nombre_persona': '', 'apellido_persona': '',
                               'descripcion_rol': 'Usuario', 'email': '','telefono_persona': '', 'imagen_src': '/static/images/avatar.png'}
                
                return render_template('AdminUser.html',datosusuarios=datosusuarios)
    # return render_template('AdminUser.html')


@app.route('/EditarLista', methods=['POST', 'GET'])
def EditarLista():
    if not session.get("username"):
        return redirect("/")
    else:
        return render_template('EditarListas.html')


@app.route('/EditarProveedores', methods=['POST', 'GET'])
def EditarProveedores():
    if not session.get("username"):
        return redirect("/")
    else:
        
        if request.method == 'POST':
            
            if request.form['submit_button'] == 'editar':
                
                # Aqui se recibe el id del proveedor para su busqueda en la base de datos, esta retorna los datos
                # del usuario
                datosProveedor=conn.obtenerProveedorById(request.form['id'])
                
                
                return render_template('EditarProveedor.html',datosProveedor=datosProveedor)
            
            elif request.form['submit_button'] == 'eliminar':
                
                # consulta para eliminar proveedor
                conn.borrarRegistrosProveedorTdAlmacen(request.form['id'])
                flash("Proveedor eliminado")
                return redirect('/Proveedores')
                
            elif request.form['submit_button']=='Añadir proveedor +':
                # Formulario en blanco para añadir proveedor
 
                datosProveedor={'id_proveedor': 0, 'nombre_proveedor': '', 'descripcion_proveedor': '', 'src_imagen': '/static/images/proveedores.png'}
                return render_template('EditarProveedor.html',datosProveedor=datosProveedor)
        

@app.route('/RecuperarPass', methods=['POST', 'GET'])
def RecuperarPass():
    if conn.validarUsuario(request.form["recuperarEmail"]) is not False:
        datosUsuario = conn.obtenerDatosUsuario(request.form['recuperarEmail'])
        nombreApellido = datosUsuario['nombre_persona'] + " " + datosUsuario['apellido_persona']
        datosEmail = enviarEmail.emailRestablecerCuenta(datosUsuario['email'], nombreApellido, datosUsuario['id_usuario'])
        response = enviarEmail.enviarCorreo(datosEmail)

    return str(response)

@app.route('/ConfirmacionNewPass', methods=['POST', 'GET'])
def ConfirmacionNewPass():
    if not session.get("username"):
        return redirect("/")
    else:
        if request.method == 'POST':
            if request.form['sign-in'] == 'Guardar':
                contrasenaActual = request.form['actualpw']
                nuevaContrasena = request.form['confirmpw']
                if conn.validarContrasena(request.form['email'], contrasenaActual) is not False:
                    conn.cambiarContraseña(conn.obtenerIDUsuario(request.form['email']), generate_password_hash(nuevaContrasena))
                    conn.cambiarEstatusUsuario(1, conn.obtenerIDUsuario(request.form['email']))
                    
                    return redirect('/')
                else:
                    return "Error"
            return render_template('Login.html')

@app.route('/CambiarPass', methods=['POST', 'GET'])
def CambiarPass():
    if not session.get("username"):
        return redirect("/")
    else:
        if request.method == 'POST':
            if request.form['submit_button'] == 'Cambiar contraseña':
                contrasenaActual = request.form['actualpw']
                nuevaContrasena = request.form['confirnpw']
                if conn.validarContrasena(session['username'], contrasenaActual) is not False:
                    conn.cambiarContraseña(request.form['id'], generate_password_hash(nuevaContrasena))
                    conn.cambiarEstatusUsuario(1, (request.form['id']))
                    flash("Contraseña cambiada correctamente")
                    return redirect('/')
                else:
                    return "Error"
        return redirect("/Home")

# Guardar datos de los usuarios. Llega des la pagina adminUser
@app.route('/GuardarUser', methods=['POST', 'GET'])
def GuardarUser():
    
    if not session.get("username"):
        return redirect("/")
    else:
        if session.get("userType")=='admin' or session.get("userType")=='superAdmin':
            if request.method == 'POST':
                if request.form['submit_button'] == 'Guardar':
                    
                    id=request.form['id']
                    nombre=request.form['nombre']
                    apellido=request.form['apellido']
                    tipoUser=request.form['selectedUsuario']    
                    if(tipoUser=="Administrador"):
                        tipoUser="admin"
                    elif(tipoUser=="Super administrador"):
                        tipoUser="superAdmin"
                    else:
                        tipoUser="usuario"; 

                    email=request.form['email']
                    telefono=request.form['telefono']
                    
                    image_src=request.files['archivo']            
                    
                    if id=="0":
                        
                        if image_src.filename !="":
                            image_src=uploader()            #Retorna Foto.png
                            image_src="/static/images/upload/"+image_src
                            
                        else:
                            image_src="/static/images/avatar.png"   # Si no se selecciona ninguna imagen, establece la imagen por defecto
                        
                        #Consulta para insert en la base de datos
                        conn.insertarPersona(nombre,apellido,telefono,email,image_src,tipoUser)
                        flash("Usuario creado correctamente")
                        
                    else:
                        if image_src.filename !="":
                            
                            image_src=uploader()            #Retorna Foto.png
                            image_src="/static/images/upload/"+image_src
                        
                            #Consulta para update en la base de datos cambiando la imagen por la seleccionada en el momento
                            conn.actualizarPersona(id,nombre,apellido,telefono,email,image_src)
                            conn.actualizarRolUsuario(conn.obtenerIDUsuarioDesdePersona(id), conn.buscarIdRol(tipoUser.strip()))
                            flash("Usuario actualizado correctamente")
                        else:
                            #Consulta para update en la base de datos sin incluir imagen, permanece la actual
                            image_src = conn.obtenerImagenPersona(id)
                            conn.actualizarPersona(id,nombre,apellido,telefono,email,image_src)
                            conn.actualizarRolUsuario(conn.obtenerIDUsuarioDesdePersona(id), conn.buscarIdRol(tipoUser.strip()))
                            flash("Usuario actualizado correctamente")
                
                    # Despues de realizar la query regresa a la pagina de usuarios 
                    return redirect('/Usuarios')
                

                elif request.form['submit_button'] == 'Cancelar':
                    return redirect('/Usuarios')
        else:
            return render_template('AccessDenied.html')
        
# Guardar datos del productos. Llega des la pagina Editar productos
@app.route('/GuardarProducto', methods=['POST', 'GET'])
def GuardarProducto():
    if not session.get("username"):
        return redirect("/")
    else:
        if request.method == 'POST':
            if request.form['submit_button'] == 'Guardar':
                id=request.form['id_producto']
                nombreProducto = request.form["nombre_producto"]
                proveedor = request.form['selectedProveedor']
                proveedor= proveedor.strip()
                descripcion =request.form["descripcion"]
                disponible=request.form["cantidad_disponible"]
                cantidad_minima=request.form["cantidad_minima"]
                calificacion=request.form["selectedCalificacion"]
                image_src=request.files['archivo']
                if id=="0":
                    
                    if image_src.filename !="":
                        image_src=uploader()
                        image_src="/static/images/upload/"+image_src
                        
                    else:
                            image_src="/static/images/Prodcuto.jpg"   # Si no se selecciona ninguna imagen, establece la imagen por defecto
                        
                    #Consulta para insert en la base de datos
                    conn.insertarProducto(nombreProducto, descripcion, calificacion, image_src, cantidad_minima, disponible, proveedor)
                    flash("Producto guardado correctamente")
                else:
                    if image_src.filename !="":
                        
                        image_src=uploader()            #Retorna Foto.png
                        image_src="/static/images/upload/"+image_src
                    
                        #Consulta para update en la base de datos cambiando la imagen por la seleccionada en el momento
                        conn.actualizarProducto(id, nombreProducto, descripcion, calificacion, image_src, cantidad_minima, disponible, proveedor)
                        flash("Producto guardado correctamente")
                    else:
                        image_src = conn.obtenerImagenProducto(id)
                        #Consulta para update en la base de datos sin incluir imagen, permanece la actual
                        conn.actualizarProducto(id, nombreProducto, descripcion, calificacion, image_src, cantidad_minima, disponible, proveedor)
                        flash("Producto guardado correctamente")
                            
                return redirect('/Productos')
            elif request.form['submit_button'] == 'Cancelar':
                return redirect('/Productos')

# Guardar datos del proveedor. Llega des la pagina Editar proveedor
@app.route('/GuardarProveedor', methods=['POST', 'GET'])
def GuardarProveedor():
    if not session.get("username"):
        return redirect("/")
    else:
        if request.method == 'POST':
            if request.form['submit_button'] == 'Guardar':
                id=request.form['id_proveedor']
                nombre_proveedor=request.form['nombre_proveedor']
                descripcion_proveedor=request.form['descripcion_proveedor']
                image_src=request.files['archivo']  
                if id=="0":
                    
                    if image_src.filename !="":
                        image_src=uploader()
                        image_src="/static/images/upload/"+image_src
                        
                    else:
                        image_src="/static/images/proveedores.png"   # Si no se selecciona ninguna imagen, establece la imagen por defecto
                        
                    #Consulta para insert en la base de datos
                    conn.insertarProveedor(nombre_proveedor,descripcion_proveedor,image_src)
                    flash("Proveedor guardado correctamente")
                else:
                        if image_src.filename !="":
                            
                            image_src=uploader()            #Retorna Foto.png
                            image_src="/static/images/upload/"+image_src
                        
                            #Consulta para update en la base de datos cambiando la imagen por la seleccionada en el momento
                            conn.actualizarProveedor(id, nombre_proveedor, descripcion_proveedor, image_src)
                            flash("Proveedor guardado correctamente")
                        else:
                            image_src = conn.obtenerImagenProveedor(id)
                            #Consulta para update en la base de datos sin incluir imagen, permanece la actual
                            conn.actualizarProveedor(id, nombre_proveedor, descripcion_proveedor, image_src)
                            flash("Proveedor guardado correctamente")

                return redirect('/Proveedores')
            
            elif request.form['submit_button'] == 'Cancelar':
                return redirect('/Proveedores')
            
# Guardar configuracion de usuario. Llega desde la pagina User
@app.route('/Guardarconfiguracion', methods=['POST', 'GET'])
def Guardarconfiguracion():
    if not session.get("username"):
        return redirect("/")
    else:
        if request.method == 'POST':
        
            
            if request.form['submit_button'] == 'Guardar':
                id=request.form['id']
                telefono=request.form['telefono']
                image_src=request.files['archivo']
                if image_src.filename !="":
                    image_src=uploader()            #Retorna Foto.png
                    image_src="/static/images/upload/"+image_src
                    #Consulta para update en la base de datos cambiando la imagen por la seleccionada en el momento. Busqueda por id
                    conn.editarConfiguracionUsuario(image_src,id,telefono)
                    flash("Configuracion de usuario guardada correctamente")
                else:
                    #Consulta para update en la base de datos sin cambiar la imagen. Busqueda por id
                    conn.editarConfiguracionUsuarioSinImagen(id,telefono)
                    flash("Configuracion de usuario guardada correctamente")    
                
                return redirect('/Home')
            elif request.form['submit_button'] == 'Cancelar':
                
                return redirect('/Home')
           
            else:
                return ('ok')
        else:
            return redirect('/Home')

def uploader():
    """Funcion para subir la imagen en el servidor
        
    """
    if not session.get("username"):
        return redirect("/")
    else:
    # obtenemos el archivo del input "archivo"
        f = request.files['archivo']
        if f and allowed_file(f.filename):

            filename = secure_filename(f.filename)
            # Guardamos el archivo en el directorio 
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Retornamos una respuesta satisfactoria
        return (filename)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
           
@app.route('/Search', methods=['POST', 'GET'])
def Search():
    if not session.get("username"):
        return redirect("/")
    else:
        if request.method == 'POST':
            textoBuscar=request.form['txtsearch']
            buscarPor=request.form['selectedSearch']
            
            if buscarPor=='Productos':
                resultadobusqueda=conn.buscarPorProducto(textoBuscar)
                
                return render_template('Search.html',textoBuscar=textoBuscar,buscarPor=buscarPor,
                                       resultadobusqueda=resultadobusqueda)
            elif buscarPor=='Proveedores':
                resultadobusqueda=conn.buscarPorProveedor(textoBuscar)
                
                return render_template('Search.html',textoBuscar=textoBuscar,buscarPor=buscarPor,
                                       resultadobusqueda=resultadobusqueda)