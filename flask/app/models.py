from sqlalchemy import UniqueConstraint, func, event
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, loginManager
from sqlalchemy.orm.attributes import get_history

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return '<User {}>'.format(self.username)

@loginManager.user_loader
def load_user(id):
    return User.query.get(int(id))
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), index=True, nullable=False)
    body = db.Column(db.String(255))
    views = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, index=True, default=func.now())
    last_edited = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='author_posts')
    replies = db.relationship('Reply', backref='post', lazy='dynamic')
    
    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(255))
    votes = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, index=True, default=func.now())
    last_edited = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='replies')
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    accepted = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return '<Reply {}>'.format(self.body)
    
@event.listens_for(Post, 'before_update')
def update_post(mapper, connection, target):
    if get_history(target, 'body').has_changes() or\
        get_history(target, 'title').has_changes():
        target.last_edited = func.now()

@event.listens_for(Reply, 'before_update')
def update_reply(mapper, connection, target):
    if get_history(target, 'body').has_changes():
        target.last_edited = func.now()

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reply_id = db.Column(db.Integer, db.ForeignKey('reply.id'), nullable=False)
    vote_type = db.Column(db.Enum('upvote', 'downvote'), nullable=False)
    
    # Unique constraint to ensure a user can vote only once on a reply
    __table_args__ = (
        UniqueConstraint('user_id', 'reply_id'),
    )

    def __repr__(self):
        return f'<Vote {self.vote_type} by User {self.user_id} on Reply {self.reply_id}>'