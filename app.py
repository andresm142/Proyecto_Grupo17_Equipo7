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
app.config['UPLOAD_FOLDER'] = './static/images/Productos-Proveedores'
Session(app)

# Instanciar módulo de conexión a la base de datos
conn = dbConnect

@app.route('/')
def login():
    return render_template('Login.html')


@app.route('/Index', methods=['GET', 'POST'])
def Index():
    if conn.validarContrasena(request.form["email"], request.form["text"]) is not False:
        session["username"] = request.form["email"]
        session["userType"] = conn.validarTipoUsuario(request.form["email"])
        return render_template('Index.html', userType=session["userType"])
    else:
        session["username"] = None
        return redirect('/')


@app.route('/Home')
def Home():
    if not session.get("username"):
        return redirect("/")
    else:
        return render_template('Index.html', userType=session["userType"])


@app.route('/Productos', methods=['POST', 'GET'])
def Productos():
    if not session.get("username"):
        return redirect("/")
    else:
        return render_template('Productos.html')


@app.route('/Listas', methods=['POST', 'GET'])
def Listas():
    if not session.get("username"):
        return redirect("/")
    else:
        return render_template('Listas.html')


@app.route('/Configuracion', methods=['POST', 'GET'])
def Configuracion():
    if not session.get("username"):
        return redirect("/")
    else:
        return render_template('User.html')


@app.route('/Proveedores', methods=['POST', 'GET'])
def Proveedores():
    if not session.get("username"):
        return redirect("/")
    else:
        return render_template('Proveedores.html')


@app.route('/Usuarios', methods=['POST', 'GET'])
def Usuarios():
    if not session.get("username"):
        return redirect("/")
    else:
        return render_template('Usuarios.html')


@app.route('/Logout', methods=['POST', 'GET'])
def Logout():
    session.pop('username', None)
    return redirect('/')


@app.route('/Editarproducto', methods=['POST', 'GET'])
def Editarproducto():
    if not session.get("username"):
        return redirect("/")
    else:
        return render_template('EditarProducto.html')


@app.route('/AdminUser', methods=['POST', 'GET'])
def AdminUser():
    print("hola")
    if not session.get("username"):
        return redirect("/")
    else:
        if request.method == 'POST':
            print("entro aqui post")
            print(request.form['submit_button'])
            if request.form.get('submit_button') == 'editar':
                id=request.form['id']
                # Aqui se recibe el id del usuario para su busqueda en la base de datos, esta retorna los datos
                # del usuario
                # connect_db = dbConnect.get_db()    #Esto lo cambias por como manejas la base de datos
                # cursor = connect_db.cursor()
                # consulta = "select * from usuario where id ='{}'".format(id)
                # cursor.execute(consulta)
                # resultado = cursor.fetchall()           #Este seria el json, a abria que cambiarlo a clave:valor
                resultado=""
                for row in resultado:
                    id=row[0]
                    nombre=row[1]
                    apellido=row[2]
                    tipoUser=row[3]
                    email=row[4]
                    telefono=row[5]
                    contrasena=row[6]
                    image_src=row[7]        # Digamos que aqui se guardo el nombre del archivo (foto1.png), debemos 
                                            # establecer la ruta para usarla en el html. Ejemplo=images/foto1.png
                resultado1=(id,nombre,apellido,tipoUser,email,telefono,contrasena,image_src)
                return render_template('AdminUser.html',resultado1=resultado1)
            
            elif request.form.get('submit_button') == 'eliminar':
                print("Boton eliminar")
                
            
        return render_template('AdminUser.html')


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
        return render_template('EditarProveedor.html')

@app.route('/RecuperarPass', methods=['POST', 'GET'])
def RecuperarPass():
    if conn.validarUsuario(request.form["recuperarEmail"]) is not False:
        datosUsuario = conn.obtenerDatosUsuario(request.form['recuperarEmail'])
        nombreApellido = datosUsuario['nombre_persona'] + " " + datosUsuario['apellido_persona']
        datosEmail = enviarEmail.prepararEmail(datosUsuario['email'], nombreApellido, datosUsuario['id_usuario'])
        response = enviarEmail.enviarCorreo(datosEmail)

    return str(response)

@app.route('/NewPass')                      
def NewPass():
    
    return render_template('CambiarContraseña.html')        

@app.route('/ConfirmacionNewPass')
def ConfirmacionNewPass():
    return render_template('Login.html')

@app.route('/GuardarProducto', methods=['POST', 'GET'])
def GuardarProducto():
    id=request.form.get('id')
    # f = request.files['archivo']
    # imagen = secure_filename(f.filename)
    nombreProducto = request.form.get("name")
    
    proveedor = request.form.get('category')
    descripcion =request.form.get("descripcion")
    cantidad=request.form.get("cantidad")
    calificacion=request.form.get("category-cal")
    print("hollaskas")
    print(id," ",nombreProducto," ",proveedor," ",descripcion," ",cantidad," ",calificacion)
    return ("ok")


# Codigo provisional. El codigo de esta ruta se puede copiar en el submit de cambiar imagen en las paginas de editar
# productos, proveedores y usuario.

@app.route("/upload", methods=['POST'])
def uploader():
 if request.method == 'POST':
  # obtenemos el archivo del input "archivo"
  f = request.files['archivo']
  filename = secure_filename(f.filename)
  # Guardamos el archivo en el directorio 
  f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
  # Retornamos una respuesta satisfactoria
  return ("")