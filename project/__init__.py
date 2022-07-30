from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask("project")
app.config['SECRET_KEY'] = os.urandom(32)
# app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_pre_ping' : True}
# app.config['SQLALCHEMY_ECHO'] = False
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://uas:uas@localhost:3306/db_akademik'

# db = SQLAlchemy(app)

from project.controllers import *
