from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
import datetime


class Logs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studentId =  db.Column(db.Integer, nullable=False)
    stream = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def toDict(self):
        return{
            'id': self.id,
            'studentId': self.studentId,
            'stream': self.stream,
            'created': self.created.strftime("%m/%d/%Y, %H:%M:%S")
        }
