from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import database

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)