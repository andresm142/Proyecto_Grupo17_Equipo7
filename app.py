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
    if not session.get("username"):
        return redirect("/")
    else:
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
        datosEmail = enviarEmail.prepararEmail(datosUsuario['email'], nombreApellido, str(datosUsuario['id_usuario']))
        response = enviarEmail.enviarCorreo(datosEmail)

    return str(response)

@app.route('/NewPass')                      
def NewPass():
    
    return render_template('CambiarContraseña.html')        

@app.route('/ConfirmacionNewPass')
def ConfirmacionNewPass():
    return render_template('Login.html')

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