from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from app.model import Face, Attendance #ini dikomen karena kada tepakai
from app import routes