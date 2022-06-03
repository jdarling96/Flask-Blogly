"""Blogly application."""

from crypt import methods
from re import template
from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def redirect_to_users():
  
    return redirect('/users')
   
@app.route('/users/new/created', methods=["POST"])
def add_user_to_database():
    first = request.form["first-name"]
    last = request.form["last-name"]
    img = request.form["img-url"]
    new_user = User(first_name=first, last_name=last, image_url=img)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')


@app.route('/users')
def users_page():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/new')
def create_new_user():
    return render_template('new_user.html')

@app.route('/users/<user_id>')
def user_page(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_info.html', user=user) 

@app.route('/users/<user_id>/edit')
def edit_user_information(user_id):
    edit = User.query.get(user_id)
    
    return render_template ('edit_user.html', edit=edit)  

@app.route('/users/<user_id>/edit/edited', methods=["POST"])
def update_user_database(user_id):
    user = User.query.get(user_id)
    first = request.form["first-name"]
    last = request.form["last-name"]
    img = request.form["img-url"]
    user.first_name = first
    user.last_name = last
    user.image_url = img
    db.session.commit()
    return redirect('/users')

@app.route('/users/<user_id>/delete')
def delete_user(user_id):
    
    User.query.filter_by(id = user_id).delete()
    db.session.commit()
    return redirect('/users')





