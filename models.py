from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    fname = db.Column(db.String(120), nullable=False)
    lname = db.Column(db.String(120), nullable=False)
    favorite = db.relationship('Favorite', backref='user', lazy=True)
    rating = db.relationship('Rating', backref='user', lazy=True)

    def toDict(self):
      return {
        "id": self.id,
        "username": self.username,
        "email": self.email,
        "password":self.password,
        "fname":self.fname,
        "lname":self.lname
      }
    
    #hashes the password parameter and stores it in the object
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')
    
    #Returns true if the parameter is equal to the object's password property
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
    
    #To String method
    def __repr__(self):
        return '<User {}>'.format(self.username)

class Instructor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prefix = db.Column(db.String(30), nullable=False)
    fname = db.Column(db.String(120), nullable=False)
    lname = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    position = db.Column(db.String(120), nullable=False)
    favorite = db.relationship('Favorite', backref='instructor', lazy=True)
    rating = db.relationship('Rating', backref='instructor', lazy=True)

    def toDict(self):
      return {
        "id": self.id,
        "prefix": self.prefix,
        "fname":self.fname,
        "lname":self.lname,
        "email": self.email,
        "position": self.position,
      }


class Favorite(db.Model):
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    instructorid = db.Column(db.Integer, db.ForeignKey('instructor.id'), primary_key=True)

    def toDict(self):
      return {
        "userid": self.userid,
        "instructorid":self.instructorid
      }

class Rating(db.Model):
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    instructorid = db.Column(db.Integer, db.ForeignKey('instructor.id'), primary_key=True)
    '''Teaching Skills'''
    rating1 = db.Column(db.Integer, nullable = False) #Presentation - Presents class material in a clear and logical sequence. 
    rating2 = db.Column(db.Integer, nullable = False) #Material Accessablity - Makes the material accessible, intelligible and meaningful. 
    rating3 = db.Column(db.Integer, nullable = False) #Material Coverage - Cover the subject matter adequately. 
    rating4 = db.Column(db.Integer, nullable = False) #Pacing - Paces lectures appropriately. 
    rating5 = db.Column(db.Integer, nullable = False) #Conciseness - Is concise.  
    rating6 = db.Column(db.Integer, nullable = False) #Practical Demonstation - Illustrates the practical application of the theory presented.
    '''Personality'''
    rating7 = db.Column(db.Integer, nullable = False) #Helpful - Is constructive and helpful in their criticism and when answering questions. 
    rating8 = db.Column(db.Integer, nullable = False) #Friendly - Easy to talk to and ask questions. 
    rating9 = db.Column(db.Integer, nullable = False) #Interesting - Generates curiosity and interest about lecture material early in the lecture.
    rating10 = db.Column(db.Integer, nullable = False) #Enthusiasm - Shows enthusiasm for the subject.
    rating11 = db.Column(db.Integer, nullable = False) #Expertise - Demonstrates expert knowledge in their subject. 

    def toDict(self):
      return {
        "userid": self.userid,
        "instructorid":self.instructorid,
        "rating1" : self.rating1,
        "rating2" : self.rating2,
        "rating3" : self.rating3,
        "rating4" : self.rating4,
        "rating5" : self.rating5,
        "rating6" : self.rating6,
        "rating7" : self.rating7,
        "rating8" : self.rating8,
        "rating9" : self.rating9,
        "rating10" : self.rating10,
        "rating11" : self.rating11
      }
