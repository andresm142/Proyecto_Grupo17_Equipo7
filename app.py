from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def login():
    return render_template('Login.html')


@app.route('/Index', methods=['POST'])
def Index():
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
    return render_template('Index.html')


@app.route('/Productos')
def Productos():
    return render_template('Productos.html')


@app.route('/Listas')
def Listas():
    return render_template('Listas.html')


@app.route('/Configuracion')
def Configuracion():
    return render_template('User.html')


@app.route('/Proveedores')
def Proveedores():
    return render_template('Proveedores.html')


@app.route('/Usuarios')
def Usuarios():
    return render_template('Usuarios.html')


@app.route('/Logout')
def Logout():
    return render_template('Login.html')


@app.route('/Editarproducto')
def Editarproducto():
    return render_template('EditarProducto.html')


@app.route('/AdminUser')
def AdminUser():
    return render_template('AdminUser.html')


@app.route('/EditarLista')
def EditarLista():
    return render_template('EditarListas.html')


@app.route('/EditarProveedores')
def EditarProveedores():
    return render_template('EditarProveedor.html')
