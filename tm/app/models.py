from datetime import datetime
from hashlib import md5
from time import time
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login

followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64))
    user_id = db.Column(db.String(120), index=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    '''
    This is not an actual database ﬁeld, but a high-level view of the relation-
    ship between users and posts.

    For a one-to-many relationship, a db.relationship ﬁeld is normally deﬁned on
    the “one” side, and is used as a convenient way to get access to the “many”.

    The ﬁrst argument to db.relationship is the model class that represents the 
    “many” side of the relationship.

    The backref argument deﬁnes the name of a ﬁeld that will be added to the ob-
    jects of the “many” class that points back at the “one” object.
    '''
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    '''
    let's say that for a pair of users linked by this relationship, 
    the left side user is following the right side user. 
    
    I'm deﬁning the relationship as seen from the left side user with the name 
    followed, because when I query this relationship from the left side I will 
    get the list of followed users.

    `backref` deﬁnes how this relationship will be accessed from the right side 
    entity. From the left side, the relationship is named followed, so from the 
    right side I am going to use the name followers to represent all the left 
    side users that are linked to the target user in the right side.

    lazy is similar to the parameter of the same name in the backref, but this 
    one applies to the left side query instead of the right side.
    '''
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        '''
        The ﬁrst argument is the followers association table, and the second ar-
        gument is the join condition.
        '''
        followed = (
            Post.query.join(
                followers,
                (followers.c.followed_id == Post.user_id)
            ).filter(
                followers.c.follower_id == self.id
            )
        )
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())
    
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
