import json
from flask import Flask, request
from flask_jwt import JWT, jwt_required, current_identity
from sqlalchemy.exc import IntegrityError
from datetime import timedelta
#from flask_mysqldb import MySQL

from models import db, User, Instructor, Favorite, Rating

''' Begin boilerplate code '''
def create_app():
  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://VCeA2YaDxo:7u3nmv2ykJ@remotemysql.com/VCeA2YaDxo' #this is where test.db is selected
  app.config['SECRET_KEY'] = "MYSECRET"
  app.config['JWT_EXPIRATION_DELTA'] = timedelta(days = 7) 
  db.init_app(app)
  return app

app = create_app()

app.app_context().push()
db.create_all(app=app)
''' End Boilerplate Code '''

''' Set up JWT here ''' #JWT for Authorization
def authenticate(uname, password):
  user = User.query.filter_by(username=uname).first() #search for the specified user
  if user and user.check_password(password):          #if user is found and password matches
    return user

#Payload for Flask JWT
def identity(payload):
  return User.query.get(payload['identity'])

jwt = JWT(app, authenticate, identity)    #initialize Flask JWT
''' End JWT Setup '''

@app.route('/signup', methods=['POST'])
def signup():
  userdata = request.get_json() # get userdata
  newuser = User(username=userdata['username'], email=userdata['email'], fname=userdata['fname'], lname=userdata['lname']) # create user object
  newuser.set_password(userdata['password']) # set password
  try:#account for errors
    db.session.add(newuser)
    db.session.commit() # save user
  except IntegrityError: # attempted to insert a duplicate user
    db.session.rollback()
    return 'username or email already exists' # error message
  return 'user created' # success

@app.route('/identify')               #identifies a user if they have a token
@jwt_required()                       #checks user token
def protected():
    return json.dumps(current_identity.fname + " " + current_identity.lname)

@app.route('/')
def index():
  return "Started!"

@app.route('/instructors', methods=['GET'])
def get_inst():
  instructors = Instructor.query.all()
  instructors = [instructor.toDict() for instructor in instructors]
  return json.dumps(instructors)

@app.route('/favorites', methods=['GET'])
@jwt_required()
def get_favorites():
  favs = Favorite.query.filter_by(userid=current_identity.id).all()
  favs = [fav.toDict() for fav in favs]
  return json.dumps(favs)
  

@app.route('/favorites', methods=['POST'])
@jwt_required()
def add_favorite():
  data = request.get_json()
  inst = Instructor.query.get(data['instid'])
  if inst == None:
    return 'Invalid instructor id or unauthorized', 403
  fav = Favorite.query.get((current_identity.id, data['instid']))
  if fav != None:
    return 'Instructor already a favorite', 403
  data = Favorite(userid=current_identity.id, instructorid=data['instid'])
  db.session.add(data)
  db.session.commit()
  return "Instructor added to favorites", 201
 
@app.route('/favorites/<instid>', methods=['DELETE'])
@jwt_required()
def delete_favorite(instid):
  fav = Favorite.query.get((current_identity.id, instid))
  if fav == None:
    return 'Invalid instructor id or not a favorite', 403
  db.session.delete(fav)
  db.session.commit()
  return "Instructor removed from favorites", 201

@app.route('/ratings/<instid>', methods=['POST'])
@jwt_required()
def add_instructor_rating(instid):
  inst = Instructor.query.get(instid)
  if inst == None:
    return 'Invalid instructor id or unauthorized', 403
  rate = Rating.query.get((current_identity.id, instid))
  if rate != None:
    return 'Already rated this insructor', 403
  data = request.get_json()
  rating = Rating(userid=current_identity.id, instructorid=instid, rating1=data["rating1"], rating2=data["rating2"], rating3=data["rating3"], rating4=data["rating4"], rating5=data["rating5"], rating6=data["rating6"], rating7=data["rating7"], rating8=data["rating8"], rating9=data["rating9"], rating10=data["rating10"], rating11=data["rating11"])
  db.session.add(rating)
  db.session.commit()
  return "Instructor rated", 201

@app.route('/ratings/<instid>', methods=['GET'])
@jwt_required()
def get_instructor_rating(instid):
  rating = Rating.query.get((current_identity.id, instid))
  if rating == None:
    'This instructor has no rating or is unauthorized', 403
  rating = rating.toDict()
  return json.dumps(rating)

@app.route('/rating/<instid>', methods=['PUT'])
@jwt_required()
def edit_lecturer_rating(instid):
  rating = Rating.query.get((current_identity.id, instid))
  if rating == None:
    return 'This instructor has no rating or is unauthorized', 403
  data = request.get_json()
  if (data['section']=="teaching"):
    rating.rating1 = data['rating1']
    rating.rating2 = data['rating2']
    rating.rating3 = data['rating3']
    rating.rating4 = data['rating4']
    rating.rating5 = data['rating5']
    rating.rating6 = data['rating6']
    db.session.add(rating)
    db.session.commit()
    return "Insructor teaching style updated", 201
  if (data['section']=="personality"):
    rating.rating7 = data['rating7']
    rating.rating8 = data['rating8']
    rating.rating9 = data['rating9']
    rating.rating10 = data['rating10']
    rating.rating11 = data['rating11']
    db.session.add(rating)
    db.session.commit()
    return "Insructor personality updated", 201
  return "Invalid request", 400

@app.route('/rating/<instid>', methods=['DELETE'])
@jwt_required()
def remove_lecturer_rating(instid):
  rating = Rating.query.get((current_identity.id, instid))
  if rating == None:
    return 'This instructor has no rating or is unauthorized', 403
  db.session.delete(rating)
  db.session.commit()
  return "Instructor deleted", 201
  pass

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)