import random
import string
from datetime import timedelta

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Função usando a biblioteca string e random para gerar uma secretkey randomica 
random_str = string.ascii_letters + string.digits + string.ascii_uppercase
key = ''.join(random.choice(random_str) for i in range(2))

db_uri = 'postgresql://darkroom9282:v2mzt67cZYDdAq@168.138.150.79:49154/todolist'

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SECRET_KEY'] = key
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)



db = SQLAlchemy(app)



