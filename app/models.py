from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# class inherits from db.Model, base class for all models from Flask-SQLAlchemy
# add generic implementations of properties required by Flask-Login with UserMixin provided by Flask-Login
# required properties included are is_authenticated, is_active, is_anonymous, and get_id()
class User(UserMixin, db.Model):
    # class fields are created as intances og the db.Column class
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # not an actual database field, but a high-level view of the relationship between users and posts
    # relationship field usually defined on the "one" side of a relationship
    # first argument is the model class that represents the "many" side of relationship
    # backref defines a field that will be added to the objects of the "many" classthat points back to the "one", post.author
    # lazy defines how the database query for the relationship will be issued
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    # __repr__ method tells Python how to print objects of this class, useful for debugging
    def __repr__(self):
        return '<User {}>'.format(self.username)

    # generate password hash and assign to user
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # compare previously generated password hash with password entered by user
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# function required to help Flask-Login load a user, id passed to the function is a string so numeric IDs need to be converted to int
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    # indexing the timestamp will be useful for retrieveing posts in chronological order
    # passing default the function datetime.utcnow NOT passing the value of the function, passing the function itself
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # reference the id from the users table used as the foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
