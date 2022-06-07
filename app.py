"""Blogly application."""




from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

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
    posts = Post.query.filter_by(user_id=user_id)
    return render_template('user_info.html', user=user, posts=posts) 

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


@app.route('/users/<user_id>/posts/new', methods=["GET", "POST"])
def new_post(user_id):
    if request.method == "GET":
        user = User.query.get(user_id)
        return render_template('add_post.html', user=user)
    else:
        title = request.form["title"]
        content = request.form["content"]
        post = Post(title=title, content=content, user_id=user_id)
        db.session.add(post)
        db.session.commit()
        return redirect(f'/users/{user_id}')



@app.route('/posts/<post_id>') 
def show_user_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template ('post_info.html', post=post)


@app.route('/posts/<post_id>/edit', methods=["GET", "POST"])
def handle_user_post_edit(post_id):
    if request.method == "GET":
        post = Post.query.get_or_404(post_id)
        return render_template('edit_post.html', post=post)
    else:
        new_title = request.form["title"]
        new_content = request.form["content"]
        post = Post.query.get(post_id)
        post.title = new_title
        post.content = new_content
        db.session.commit()
        return redirect(f'/users/{post.user_id}')
    


@app.route('/posts/<post_id>/delete', methods=["GET", "POST"])
def delete_user_post(post_id):
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{post.user_id}') 









