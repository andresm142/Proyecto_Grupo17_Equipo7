from flask import Flask, render_template, request, redirect, url_for
from werkzeug.wrappers import response

app=Flask(__name__)

@app.route('/')
def login():
    return render_template('Login.html')

@app.route('/master', methods=['POST'])
def master():
    print(request.form)
    usuario= request.form['email']
    clave=request.form['clave']
    print(usuario+' '+clave)
    return redirect(url_for('MasterPage.html'))
    # return render_template('MasterPage.html')

app.run(debug = True)