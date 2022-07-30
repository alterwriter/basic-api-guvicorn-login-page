from project import app
from flask import render_template, redirect, url_for, request, session
from project.config.Database import *
from project.config.Hash import Hash

@app.route('/', methods = ['GET'])
def index():
    if 'login' in session:
        return redirect('/home')
        
    return redirect("/login")

@app.route('/login', methods=['GET'])
def login():
    return render_template('auth/login.html')

@app.route('/login', methods=['POST'])
def login_action():
    username = request.form['username']
    passwd = request.form['pass']

    user = UserModel.query.filter_by(username=username).first()
    if not user:
        return redirect("/login")
    
    if Hash().cekHash(user.password, passwd):
        session['login'] = True
        session['id'] = user.id
        session['name'] = user.name
        session['username'] = user.username

        return redirect("/home")
    
    return redirect("/login")

@app.route('/logout', methods=['GET'])
def logout_action():
    if 'login' in session:
        del session['login']
        del session['name']
        del session['username']
    
    return redirect('/login')