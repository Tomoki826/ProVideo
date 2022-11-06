from flask_sqlalchemy import SQLAlchemy
from __init__ import app

db = SQLAlchemy(app)
from .models import employee

from __init__ import db
with app.app_context():
    db.create_all()