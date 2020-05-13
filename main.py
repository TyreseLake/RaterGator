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
    if current_user.is_authenticated:
        flash("Logged in successfully.")
        return render_template('index.html')
    signup = request.args.get('signup')
    if signup is not None:
        return render_template('login.html', signup = True)
    return  render_template('login.html', signup = False)

@app.route('/auth', methods=['POST'])
def authentication():
    data = request.get_json()
    user = User.query.filter_by(username = data['username']).first()
    if (user and user.check_password(data['password']) or (current_user.is_authenticated)): # check credentials
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

@app.route('/identify', methods=['GET'])            #identifies a user if they have a token
@login_required                                      #checks user token
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

'''
#Get Favorites - used for debugging
@app.route('/favorites', methods=['GET'])
@login_required
def get_favorites():
    favs = Favorite.query.filter_by(userid=current_user.id).all()
    favs = [fav.toDict() for fav in favs]
    return json.dumps(favs)
'''

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

@app.route('/myratings/<instid>', methods=['POST'])
@login_required
def add_instructor_rating(instid):
    inst = Instructor.query.get(instid)
    if inst == None:
        flash ('Invalid instructor id or unauthorized')
        return 'Invalid instructor id or unauthorized', 401
    rate = Rating.query.get((current_user.id, instid))
    if rate != None:
        flash ('Already rated this insructor')
        return 'Already rated this insructor', 403
    data = request.get_json()
    rating = Rating(userid=current_user.id, instructorid=instid, rating1=data["rating1"], rating2=data["rating2"], rating3=data["rating3"], rating4=data["rating4"], rating5=data["rating5"], rating6=data["rating6"], rating7=data["rating7"], rating8=data["rating8"], rating9=data["rating9"], rating10=data["rating10"], rating11=data["rating11"])
    db.session.add(rating)
    db.session.commit()
    flash ('Instructor rated')
    return "Instructor rated", 201

@app.route('/myratings/<instid>', methods=['GET'])
@login_required
def get_instructor_rating(instid):
    inst = Instructor.query.get(instid)
    if inst == None:
        return 'Invalid instructor id or unauthorized', 403
    rating = Rating.query.get((current_user.id, instid))
    print(rating)
    if rating == None:
        return 'This instructor has no rating or is unauthorized', 403
    inst = inst.toDict()
    rating = rating.toDict()
    return json.dumps(rating)

@app.route('/ratings/<instid>', methods=['GET'])
def get_instructor_avg_rating(instid):
    inst = Instructor.query.get(instid)
    if inst == None:
        return 'Invalid instructor id or unauthorized', 403
    inst = inst.toDict()
    if current_user.is_authenticated:
        myRating = Rating.query.get((current_user.id, instid))
        if myRating != None:
            myRating = myRating.toDict()

        fav = Favorite.query.get((current_user.id, instid))
        if fav != None:
            fav = True
        else:
            fav = False
    else:
        myRating = None
        fav = None

    ratings = Rating.query.filter_by(instructorid=instid).all()

    if len(ratings) == 0:
        rating = None
        return render_template('ratings.html', inst = inst, rating = rating, myRating=myRating, fav=fav)

    avgRatings = {
        "rating1" : 0.0,
        "rating2" : 0.0,
        "rating3" : 0.0,
        "rating4" : 0.0,
        "rating5" : 0.0,
        "rating6" : 0.0,
        "rating7" : 0.0,
        "rating8" : 0.0,
        "rating9" : 0.0,
        "rating10" : 0.0,
        "rating11" : 0.0
    }
    
    for rating in ratings:
        rating = rating.toDict()
        avgRatings["rating1"] += rating["rating1"]
        avgRatings["rating2"] += rating["rating2"]
        avgRatings["rating3"] += rating["rating3"] 
        avgRatings["rating4"] += rating["rating4"]
        avgRatings["rating5"] += rating["rating5"]
        avgRatings["rating6"] += rating["rating6"]
        avgRatings["rating7"] += rating["rating7"]
        avgRatings["rating8"] += rating["rating8"]
        avgRatings["rating9"] += rating["rating9"]
        avgRatings["rating10"] += rating["rating10"]
        avgRatings["rating11"] += rating["rating11"]

    count = len(ratings)
    
    avgRatings["rating1"] = avgRatings["rating1"]/count
    avgRatings["rating2"] = avgRatings["rating2"]/count
    avgRatings["rating3"] = avgRatings["rating3"]/count
    avgRatings["rating4"] = avgRatings["rating4"]/count
    avgRatings["rating5"] = avgRatings["rating5"]/count
    avgRatings["rating6"] = avgRatings["rating6"]/count
    avgRatings["rating7"] = avgRatings["rating7"]/count
    avgRatings["rating8"] = avgRatings["rating8"]/count
    avgRatings["rating9"] = avgRatings["rating9"]/count
    avgRatings["rating10"] = avgRatings["rating10"]/count
    avgRatings["rating11"] = avgRatings["rating11"]/count
        
    return render_template('ratings.html', inst = inst, rating = avgRatings, myRating = myRating, fav=fav)

@app.route('/myratings/<instid>', methods=['PUT'])
@login_required
def edit_lecturer_rating(instid):
    rating = Rating.query.get((current_user.id, instid))
    if rating == None:
        flash('This instructor has no rating or is unauthorized')
        return 'This instructor has no rating or is unauthorized', 401
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
        flash('Insructor teaching style updated')
        return "Insructor teaching style updated", 201
    if (data['section']=="personality"):
        rating.rating7 = data['rating7']
        rating.rating8 = data['rating8']
        rating.rating9 = data['rating9']
        rating.rating10 = data['rating10']
        rating.rating11 = data['rating11']
        db.session.add(rating)
        db.session.commit()
        flash('Insructor personality updated')
        return "Insructor personality updated", 201
    flash('Invalid request')
    return "Invalid request", 400

@app.route('/myratings/<instid>', methods=['DELETE'])
@login_required
def remove_lecturer_rating(instid):
    rating = Rating.query.get((current_user.id, instid))
    if rating == None:
        return 'This instructor has no rating or is unauthorized', 403
    db.session.delete(rating)
    db.session.commit()
    flash('Instructor rating removed')
    return "Instructor deleted", 201

@app.route('/about')
def aboutus():
    return render_template('aboutus.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)