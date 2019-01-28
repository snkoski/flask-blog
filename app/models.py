from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5


# followers table is an auxiliary table with no data but foreign keys so it doesn't need an associated model class
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)
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
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    # self-referential relationship, user to user
    # secondary configures the association table
    # primaryjoin indicates the condition that links the left side entity (follower user) with the association table
    # secondaryjoin indicates the condition that links the right side entity (followed user)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic'
    )


    # __repr__ method tells Python how to print objects of this class, useful for debugging
    def __repr__(self):
        return '<User {}>'.format(self.username)

    # generate password hash and assign to user
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # compare previously generated password hash with password entered by user
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # create avatar for user by using md5 hash of their email with gravatar
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    # methods to check if already following, start following, and stop following users
    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    # invoke join operation on Post table, first argument is table to join with and second argument is the join condition. create temporary table that combines data from posts and followers tables according to the merge condition.
    # filter posts by selecting ones where the follower_id is the same as the current users id
    # sort the posts by their timestamp newest to oldest.
    def followed_posts(self):
        return Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id).order_by(
                    Post.timestamp.desc())

    def user_posts(self):
        own = Post.query.filter_by(user_id=self.id)
        return own.order_by(Post.timestamp.desc())

# function required to help Flask-Login load a user, id passed to the function is a string so numeric IDs need to be converted to int
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    body = db.Column(db.String(1000))
    # indexing the timestamp will be useful for retrieveing posts in chronological order
    # passing default the function datetime.utcnow NOT passing the value of the function, passing the function itself
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # reference the id from the users table used as the foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
