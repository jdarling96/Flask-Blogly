"""Seed file to make sample data for User db."""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add pets

joshua = User(first_name='Josh', last_name='Darling',image_url="https://media.istockphoto.com/vectors/profile-picture-whith-red-tie-unknown-person-silhouette-vector-id526811989")


# Add new objects to session, so they'll persist
db.session.add(joshua)


# Commit--otherwise, this never gets saved!
db.session.commit()
