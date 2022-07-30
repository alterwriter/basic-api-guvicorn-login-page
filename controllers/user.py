import os
from project import app
from flask import render_template, redirect, url_for, request, session
from project.config.Database import *
from project.config.Hash import Hash

from functools import wraps

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'login' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/login')

    return wrap

@app.route("/home")
@login_required
def home_index():
    return render_template("home/index.html")

@app.route("/users")
@login_required
def user_index():
    users = UserModel.query.all()
    return render_template("home/user.html", users=users)

@app.route("/users/create")
@login_required
def user_add():
    return render_template("home/form.html", card_title="Add User")

@app.route("/users/create", methods=["POST"])
@login_required
def user_add_action():
    name = request.form['name']
    username = request.form['username']
    password = request.form['password']
    permission = request.form.getlist("permission")

    user = UserModel(name=name, username=username, password=Hash().getHash(password), read_key=Hash().md5(os.urandom(32)) if 'read' in permission else None, write_key=Hash().md5(os.urandom(32)) if 'write' in permission else None, is_active=1)
    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/edit/<id>")
@login_required
def user_edit(id):
    user = UserModel.query.filter_by(id=id).first()
    if not user:
        return redirect("/users")

    return render_template("home/form.html", card_title="Edit User", user=user)

@app.route("/users/edit/<id>", methods=["POST"])
@login_required
def user_edit_action(id):
    user = UserModel.query.filter_by(id=id).first()
    if not user:
        return redirect("/users")

    name = request.form['name']
    username = request.form['username']
    password = request.form['password']
    permission = request.form.getlist("permission")

    user.name = name
    user.username = username
    if password:
        user.password = Hash().getHash(password)
    
    if 'write' in permission:
        user.write_key = Hash().md5(os.urandom(32))
    else:
        user.write_key = None
    
    if 'read' in permission:
        user.read_key = Hash().md5(os.urandom(32))
    else:
        user.read_key = None

    db.session.commit()

    return redirect("/users")

@app.route("/users/delete/<id>")
@login_required
def user_delete(id):
    uk = UserModel.query.filter_by(id=id)
    user = uk.first()
    if not user:
        return redirect("/users")
    
    uk.delete()
    db.session.commit()

    return redirect("/users")
