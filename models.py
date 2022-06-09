


from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

"""Models for Blogly."""

class User(db.Model):
    """Site user."""

    __tablename__ = 'users'

    def __repr__(self):
        u = self
        return f"<User id={u.id} first_name={u.first_name} last_name={u.last_name} image_url={u.image_url}>"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String(20), nullable=False)

    last_name = db.Column(db.String(20), nullable=False)

    image_url = db.Column(db.String(200), unique=True)

    posts = db.relationship("Post", backref="user", cascade="all, delete")


class Post(db.Model):
    """Blog post."""

    __tablename__ = 'posts'

    def __repr__(self):
        u = self
        return f"<User id={u.id} title={u.title} content={u.content} created_at={u.created_at} user_id={u.user_id}>"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(50), nullable=False)  

    content = db.Column(db.Text)

    created_at = db.Column(db.DateTime(timezone=True), default=func.now())

    time_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) 

    

    relation = db.relationship('PostTag', backref='posts')

    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")

class Tag(db.Model):
    """Tag that can be added to posts."""

    __tablename__ = "tags"

    def __repr__(self):
        u = self
        return f"<Tag id={u.id} name={u.id}>"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(15), unique=True)

    posts = db.relationship('Post', secondary="post_tag", cascade="all, delete", backref='tags') 


class PostTag(db.Model):
    """Tag on a post."""

    __tablename__ = 'post_tag'

    def __repr__(self):
        u = self
        return f"<PostTag post_id={u.post_id} tag_id={u.tag_id}>"

    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id'), primary_key=True)

    tag_id = db.Column(db.Integer, db.ForeignKey(
        'tags.id'), primary_key=True)       









