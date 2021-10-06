from flask import Flask, render_template

app=Flask(__name__)
@app.route('/')
def wtv():
    return render_template('Login.html')