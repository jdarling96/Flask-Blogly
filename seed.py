"""Seed file to make sample data for User db."""


from models import Post, User, db, Tag, PostTag
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
Post.query.delete()
Tag.query.delete()
PostTag.query.delete()


# Add users
joshua = User(first_name='Josh', last_name='Darling',image_url="https://media.istockphoto.com/vectors/profile-picture-whith-red-tie-unknown-person-silhouette-vector-id526811989")
michael = User(first_name='Michael', last_name='Scott', image_url='https://toppng.com/uploads/preview/michael-scott-michael-scott-steve-carell-115629433348awbpe6n7a.png')
jim = User(first_name='Jim', last_name='Halpert', image_url='https://i1.sndcdn.com/avatars-000584794419-aw5utn-t500x500.jpg')

db.session.add_all([joshua, michael, jim])
db.session.commit()

# Add posts
first_post = Post(title='My First Post', content='Oh hi there!', user_id=1)
top_gun = Post(title='The Second Top Gun is Better', content='Go see the second Top Gun. You wont be dissapointed!', user_id=2)
hire = Post(title='They Should Hire the Creator of this', content='What a cool website!', user_id=3)

db.session.add_all([first_post, top_gun, hire])
db.session.commit()

# Add tags
movie = Tag(name='Movie')
hello = Tag(name='Hello')
employment = Tag(name='Employment')

db.session.add_all([movie, hello, employment])
db.session.commit()

# Add post_tags
first = PostTag(post_id=top_gun.id, tag_id=movie.id)
second = PostTag(post_id=first_post.id, tag_id=hello.id)
third = PostTag(post_id=hire.id, tag_id=employment.id)

db.session.add_all([first, second, third])
db.session.commit()

