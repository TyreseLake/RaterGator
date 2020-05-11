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

@app.route('/data', methods=['GET'])
def getData():
  token = request.args.get('token')
  res = 'Hello token='+token if token else "Hello"
  return res

@app.route('/data', methods=['POST'])
def addData():
  data = request.json
  res = 'Hello data='+json.dumps(data) if data else "Hello"
  return res, 201

@app.route('/data/:id', methods=['DELETE'])
def removeData(id):
  res = 'id '+id+' Deleted!'
  return res, 204

@app.route('/data/:id', methods=['UPDATE'])
def updateData(id):
  data = request.json
  res = 'id '+id
  res += ' Hello data='+json.dumps(data) if data else "Hello"
  return res, 201

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)