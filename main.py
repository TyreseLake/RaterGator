import json
from flask_cors import CORS
from flask import Flask, request, render_template, flash, redirect, url_for
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from sqlalchemy.exc import IntegrityError

from models import db, User, Instructor, Favorite, Rating

''' Begin Flask Login Functions '''
login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
''' End Flask Login Functions '''

''' Begin boilerplate code '''
def create_app():
    app = Flask(__name__, static_url_path='')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://VCeA2YaDxo:7u3nmv2ykJ@remotemysql.com/VCeA2YaDxo'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SECRET_KEY'] = "MYSECRET"
    login_manager.init_app(app)
    CORS(app)
    db.init_app(app)
    return app

app = create_app()

app.app_context().push()

''' End Boilerplate Code '''

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    signup = request.args.get('signup')
    if signup is not None:
        return render_template('login.html', signup = True)
    return  render_template('login.html', signup = False)

@app.route('/auth', methods=['POST'])
def authentication():
    data = request.get_json()
    user = User.query.filter_by(username = data['username']).first()
    if user and user.check_password(data['password']): # check credentials
        flash('Logged in successfully.') # send message to next page
        login_user(user) # login the user
        return "Logged in successfully", 200 # redirect to main page if login successful
    else:
        flash('Invalid username or password') # send message to next page
        return "Invalid username or password", 403

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.')
    return redirect('/')

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
        flash('Username or email already exists')
        return 'username or email already exists', 401 # error message
    flash('User created')
    return 'user created', 201 # success

app.route('/identify')               #identifies a user if they have a token
@login_required                       #checks user token
def protected():
    return json.dumps(current_user.fname + " " + current_user.lname)

@app.route('/instructors', methods=['GET'])
def get_inst():
    instructors = Instructor.query.all()
    instructors = [instructor.toDict() for instructor in instructors]
    if current_user.is_authenticated:
        favs = Favorite.query.filter_by(userid=current_user.id).all()
        favs = [fav.toDict() for fav in favs]
    else:
        favs = None
    return render_template("instructors.html", instructors = instructors, favorites = favs)

@app.route('/favorites', methods=['GET'])
@login_required
def get_favorites():
    favs = Favorite.query.filter_by(userid=current_user.id).all()
    favs = [fav.toDict() for fav in favs]
    return json.dumps(favs)

@app.route('/favorites', methods=['GET'])
@login_required
def get_favorites():
    favs = Favorite.query.filter_by(userid=current_user.id).all()
    favs = [fav.toDict() for fav in favs]
    return json.dumps(favs)

@app.route('/favorites/<instid>', methods=['POST'])
@login_required
def add_favorite(instid):
    data = request.get_json()
    inst = Instructor.query.get(instid)
    if inst == None:
        return 'Invalid instructor id or unauthorized', 403
    fav = Favorite.query.get((current_user.id, instid))
    if fav != None:
        return 'Instructor already a favorite', 403
    data = Favorite(userid=current_user.id, instructorid=instid)
    db.session.add(data)
    db.session.commit()
    return "Instructor added to favorites", 201
 
@app.route('/favorites/<instid>', methods=['DELETE'])
@login_required
def delete_favorite(instid):
    fav = Favorite.query.get((current_user.id, instid))
    if fav == None:
        return 'Invalid instructor id or not a favorite', 403
    db.session.delete(fav)
    db.session.commit()
    return "Instructor removed from favorites", 201

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)