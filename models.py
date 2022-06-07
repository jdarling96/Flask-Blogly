

from time import timezone
from xmlrpc.client import DateTime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

"""Models for Blogly."""

class User(db.Model):

    __tablename__ = 'users'

    def __repr__(self):
        u = self
        return f"<User id={u.id} first_name={u.first_name} last_name={u.last_name} image_url={u.image_url}>"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String(20), nullable=False)

    last_name = db.Column(db.String(20), nullable=False)

    image_url = db.Column(db.String(200), unique=True)


class Post(db.Model):

    __tablename__ = 'posts'

    def __repr__(self):
        u = self
        return f"<User id={u.id} title={u.title} content={u.content} created_at={u.created_at} user_id={u.user_id}>"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(50), nullable=False)  

    content = db.Column(db.Text)

    created_at = db.Column(db.DateTime(timezone=True), default=func.current_timestamp())

    time_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) 

    user = db.relationship('User', backref='posts')







