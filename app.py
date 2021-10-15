import secrets
import dbConnect
from flask import Flask, render_template, request, session, redirect
from flask_session import Session

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(20)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def login():
    return render_template('Login.html')


@app.route('/Index', methods=['GET', 'POST'])
def Index():
    # Variables para almacenar el tipo de usuario (usuario, admin, superadmin)
    global userType
    # Instanciar y crear la conexión hacia la base de datos.
    conn = dbConnect.crearConexion()

    if validarUsuario(conn, request.form["email"], request.form["text"]):
        userType = "usuario"
        session["username"] = request.form["email"]
        return render_template('Index.html', userType=userType)
    else:
        session["username"] = None
        return render_template('Login.html')


@app.route('/Home')
def Home():
    if not session.get("username"):
        return redirect("/")
    else:
        return render_template('Index.html', userType=userType)


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


def validarUsuario(conn, usuario, password):
    cursor = conn.cursor()

    queryUser = cursor.execute("SELECT email FROM Persona WHERE email = '%s'" % usuario).fetchone()
    queryPass = cursor.execute("SELECT usr.contrasena FROM Persona per, Usuario usr WHERE usr.id_persona = per.id_persona AND per.email = '%s'" % usuario).fetchone()

    if queryUser is not None and queryPass is not None:
        queryUser = queryUser[0]
        queryPass = queryPass[0]

    if queryUser == usuario and queryPass == password:
        conn.close()
        return True
    else:
        conn.close()
        return False
