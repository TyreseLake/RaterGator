from main import app
from models import db

db.create_all(app=app)

print('database initialized!')