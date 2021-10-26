import re
import secrets, os
import dbConnect
from flask import Flask, jsonify, render_template, request, session, redirect
from flask_session import Session
from werkzeug.utils import secure_filename

import enviarEmail

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(20)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['UPLOAD_FOLDER'] = './static/images/upload'
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
                id=request.form['id']
                # consulta para eliminar producto
                print("Boton eliminar")
                return redirect('/Productos')
                
            elif request.form['submit_button']=='Añadir +':
                # Formulario en blanco para añadir producto
                id=""
                nombre_producto=""
                proveedor=""
                descripcion=""
                cantidad=""
                calificacion=""
                proveedores=conn.listaProveedores()               
                datosProducto={'id_producto':'','id_proveedor':'','nombre_proveedor': 'Proveedor','calificacion':1,'src_imagen':'/static/images/Producto.jpg'}
                return render_template('EditarProducto.html',datosProducto=datosProducto,proveedores=proveedores)
                
            elif request.form['submit_button'] == 'Disponible':
                
                textoBuscar='productos'
                buscarPor='Disponibles'
           
                resultadobusqueda=''        #Consulta para Disponibles. se considera Disponible cuando la cantiada 
                                            # diponible es mayor a la cantidad minima en bodega
                
                return render_template('Search.html',textoBuscar=textoBuscar,buscarPor=buscarPor,
                                       resultadobusqueda=resultadobusqueda)
                # consulta para buscar los productos disponibles
                print("Disponible")
            elif request.form['submit_button'] == 'No Disponible':
                textoBuscar='productos'
                buscarPor='No Disponibles'
           
                resultadobusqueda=''     # Consulta para No disponible, se considera no disponible cuando la cantiada 
                                         # diponible es menor a la cantidad minima en bodega
                return render_template('Search.html',textoBuscar=textoBuscar,buscarPor=buscarPor,
                                       resultadobusqueda=resultadobusqueda)
 
 
@app.route('/AdminUser', methods=['POST', 'GET'])
def AdminUser():
    if not session.get("username"):
        return redirect("/")
    else:
        if request.method == 'POST':
            
            if request.form.get('submit_button') == 'editar':
                id=request.form['id']
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
                return redirect('/Usuarios')
            elif request.form.get('submit_button')=='Añadir usuario +':
                id=""
                nombre=""
                apellido=""
                tipoUser="Usuario"
                email=""
                telefono=""
                contrasena=""
                image_src="/static/images/avatar.png"                            
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
                
                return redirect('/Proveedores')
                
            elif request.form['submit_button']=='Añadir proveedor +':
                # Formulario en blanco para añadir proveedor
                # id=""
                # nombre_proveedor=""
                # descripcion=""
                # image_src="/static/images/proveedor.png"                            #Para pruebas
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

@app.route('/NewPass')                      
def NewPass():
    
    return render_template('CambiarContrasena.html')        

@app.route('/ConfirmacionNewPass')
def ConfirmacionNewPass():
    return render_template('Login.html')

@app.route('/CambiarPass', methods=['POST', 'GET'])
def CambiarPass():
    if not session.get("username"):
        return redirect("/")
    else:
        if request.method == 'POST':
            if request.form['submit_button'] == 'Cambiar contraseña':
                contrasenaActual = request.form['contrasenaActual']
                nuevaContrasena = request.form['nuevaContrasena']
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
                        
                        
                    else:
                        if image_src.filename !="":
                            
                            image_src=uploader()            #Retorna Foto.png
                            image_src="/static/images/upload/"+image_src
                        
                            #Consulta para update en la base de datos cambiando la imagen por la seleccionada en el momento
                            conn.insertarPersona(nombre,apellido,telefono,email,image_src,tipoUser)
                        else:
                            
                            #Consulta para update en la base de datos sin incluir imagen, permanece la actual
                            conn.insertarPersona(nombre,apellido,telefono,email,image_src,tipoUser)
                            
                
                    # Despues de realizar la query regresa a la pagina de usuarios 
                    return redirect('/Usuarios')
                
                # elif request.form['submit_button'] == 'Restablecer contraseña usuario':
                #     # Codigo para enviar correo con la contraseña nueva
                #     return redirect('/Usuarios')
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
                if id=="":
                    
                    if image_src.filename !="":
                        image_src=uploader()
                        image_src="/static/images/upload/"+image_src
                        
                    else:
                            image_src="/static/images/Prodcuto.jpg"   # Si no se selecciona ninguna imagen, establece la imagen por defecto
                        
                    #Consulta para insert en la base de datos
                    print(nombreProducto, descripcion, calificacion, image_src, cantidad_minima, disponible, proveedor)
                    conn.insertarProducto(nombreProducto, descripcion, calificacion, image_src, cantidad_minima, disponible, proveedor)
                   
                else:
                        if image_src.filename !="":
                            
                            image_src=uploader()            #Retorna Foto.png
                            image_src="/static/images/upload/"+image_src
                        
                            #Consulta para update en la base de datos cambiando la imagen por la seleccionada en el momento
                            conn.insertarProducto(nombreProducto, descripcion, calificacion, image_src, cantidad_minima, disponible, proveedor)
                        else:
                            
                            #Consulta para update en la base de datos sin incluir imagen, permanece la actual
                            # conn.insertarProducto(nombreProducto, descripcion, calificacion, image_src, cantidad_minima, disponible, proveedor)
                            pass
                            
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
                else:
                        if image_src.filename !="":
                            
                            image_src=uploader()            #Retorna Foto.png
                            image_src="/static/images/upload/"+image_src
                        
                            #Consulta para update en la base de datos cambiando la imagen por la seleccionada en el momento
                            conn.insertarProveedor(nombre_proveedor,descripcion_proveedor,image_src)
                        else:
                            
                            #Consulta para update en la base de datos sin incluir imagen, permanece la actual
                            conn.insertarProveedor(nombre_proveedor,descripcion_proveedor,image_src)
                                   
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
                else:
                    #Consulta para update en la base de datos sin cambiar la imagen. Busqueda por id
                    conn.editarConfiguracionUsuarioSinImagen(id,telefono)
                    
                
                return redirect('/Home')
            elif request.form['submit_button'] == 'Cancelar':
                
                return redirect('/Home')
            elif request.form['submit_button'] == 'Cambiar contraseña':
                id=request.form['id']
                actualpw=request.form['actualpw']
                newpw=request.form['confirnpw']
                # Consulta para cambiar la contraseña del usuario por medio de su id
                
                # if conn.constraseñaActual(id,actualpw)==True:
                #     conn.cambiarContraseña(id,newpw)
                #     return redirect('/Home')
                
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
        filename = secure_filename(f.filename)
        # Guardamos el archivo en el directorio 
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Retornamos una respuesta satisfactoria
        return (filename)

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