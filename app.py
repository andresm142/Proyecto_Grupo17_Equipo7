from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def login():
    return render_template('Login.html')


@app.route('/Index', methods=['POST'])
def Index():
    global userType
    if request.form["email"] == "alope@uninorte.edu.co":
        userType = "usuario"
    elif request.form["email"] == "jfonsecad@uninorte.edu.co":
        userType = "usuario"
    elif request.form["email"] == "andresmf@uninorte.edu.co":
        userType = "admin"
    elif request.form["email"] == "menesesac@uninorte.edu.co":
        userType = "admin"
    elif request.form["email"] == "jennifferg@uninorte.edu.co":
        userType = "superAdmin"
    else:
        userType = "usuario"

    return render_template('Index.html', userType=userType)


@app.route('/Home')
def Home():
    return render_template('Index.html', userType=userType)


@app.route('/Productos', methods=['POST','GET'])
def Productos():
    return render_template('Productos.html')


@app.route('/Listas', methods=['POST','GET'])
def Listas():
    return render_template('Listas.html')


@app.route('/Configuracion', methods=['POST','GET'])
def Configuracion():
    return render_template('User.html')


@app.route('/Proveedores', methods=['POST','GET'])
def Proveedores():
    return render_template('Proveedores.html')


@app.route('/Usuarios', methods=['POST','GET'])
def Usuarios():
    return render_template('Usuarios.html')


@app.route('/Logout', methods=['POST','GET'])
def Logout():
    return render_template('Login.html')


@app.route('/Editarproducto', methods=['POST','GET'])
def Editarproducto():
    return render_template('EditarProducto.html')


@app.route('/AdminUser', methods=['POST','GET'])
def AdminUser():
    return render_template('AdminUser.html')


@app.route('/EditarLista', methods=['POST','GET'])
def EditarLista():
    return render_template('EditarListas.html')


@app.route('/EditarProveedores', methods=['POST','GET'])
def EditarProveedores():
    return render_template('EditarProveedor.html')
