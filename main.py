import json
from flask_cors import CORS
from flask import Flask, request, render_template
from sqlalchemy.exc import IntegrityError

from models import db, Logs

''' Begin boilerplate code '''
def create_app():
  app = Flask(__name__, static_url_path='')
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
  app.config['SECRET_KEY'] = "MYSECRET"
  CORS(app)
  db.init_app(app)
  return app

app = create_app()

app.app_context().push()

''' End Boilerplate Code '''

@app.route('/')
def index():
  return render_template('home.html')

@app.route('/app')
def client_app():
  return app.send_static_file('app.html')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)