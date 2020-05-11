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

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)