"""Blogly application."""



from crypt import methods
from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "1234"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def redirect_to_users():
    """Show recent list of posts, most-recent first."""
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("homepage.html", posts=posts)


@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""

    return render_template('404.html'), 404    

##############################################################################
# User route

@app.route('/users/new/created', methods=["POST"])
def add_user_to_database():
    first = request.form["first-name"]
    last = request.form["last-name"]
    img = request.form["img-url"]
    new_user = User(first_name=first, last_name=last, image_url=img or None)
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

@app.route('/users/<int:user_id>')
def user_page(user_id):
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user_id)
    return render_template('user_info.html', user=user, posts=posts) 

@app.route('/users/<int:user_id>/edit')
def edit_user_information(user_id):
    edit = User.query.get(user_id)
    
    return render_template ('edit_user.html', edit=edit)  

@app.route('/users/<int:user_id>/edit/edited', methods=["POST"])
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


@app.route('/users/<int:user_id>/posts/new', methods=["GET", "POST"])
def new_post(user_id):
    if request.method == "GET":
        user = User.query.get(user_id)
        tags = Tag.query.all()
        return render_template('add_post.html', user=user, tags=tags)
    else:
       user = User.query.get_or_404(user_id)
       tag_ids = [int(num) for num in request.form.getlist("tag")]
       tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user,
                    tags=tags)

    db.session.add(new_post)
    db.session.commit()
    return redirect(f'/users/{user_id}')



@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')




##############################################################################
# Posts route

@app.route('/posts/<int:post_id>') 
def show_user_post(post_id):
    post = Post.query.get_or_404(post_id)
    tags = post.tags
    return render_template ('post_info.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=["GET", "POST"])
def handle_user_post_edit(post_id):
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    if request.method == "GET":
        return render_template('edit_post.html', post=post, tags=tags)
    else:
        new_title = request.form["title"]
        new_content = request.form["content"]
        post.title = new_title
        post.content = new_content

        tag_ids = [int(num) for num in request.form.getlist("tag")]
        post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
        
        db.session.commit()
        return redirect(f'/users/{post.user_id}')
    


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_user_post(post_id):
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/users') 

##############################################################################
# Tags route

@app.route('/tags')
def list_all_tags():
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)    

@app.route('/tags/<int:tag_id>')
def tag_details(tag_id):
    tags = Tag.query.get_or_404(tag_id)
    titles = tags.posts
    return render_template('tags_info.html', titles=titles, tags=tags)  

@app.route('/tags/new', methods=["GET", "POST"] )
def create_tag():
    if request.method == "GET":
        return render_template('new_tag.html')
    else:
        name = request.form["name"]
        create_tag = Tag(name=name)
        db.session.add(create_tag)
        db.session.commit()
        return redirect('/tags')    

@app.route('/tags/<int:tag_id>/edit', methods=["GET", "POST"])
def edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    if request.method == "GET":
        return render_template('edit_tag.html',tag=tag)
    else:
        new_name = request.form["name"]
        tag.name = new_name
        db.session.commit()
        return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=["GET", "POST"])  
def delete_tag(tag_id):
    delete_tag = Tag.query.get_or_404(tag_id)
    db.session.delete(delete_tag)
    db.session.commit()
    return redirect('/tags')











