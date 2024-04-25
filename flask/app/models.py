from sqlalchemy import UniqueConstraint, func, event
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, loginManager
from sqlalchemy.orm.attributes import get_history
from app.tools import convert_timezone

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    suburb = db.Column(db.String(50))
    profile_image = db.Column(db.String(255))
    posts = db.relationship('Post', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    interested_topics = db.Column(db.String(200))
    points = db.Column(db.Integer, default=0)


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
    body = db.Column(db.String(255) , nullable=False)
    views = db.Column(db.Integer, default=0)
    votes = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, index=True, default=func.now())
    last_edited = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    replies = db.relationship('Reply', backref='post', lazy='dynamic', cascade='all, delete-orphan')
    topic = db.Column(db.String(100), nullable=False)

    @property
    def user(self):
        return User.query.get(self.user_id)

    @property
    def real_timestamp(self):
        # return self._real_timestamp(self.user.timezone if self.user.timezone else None)
        return self._real_timestamp(None)
    
    def _real_timestamp(self, timezone):
        if not self.timestamp:
            return None
        return convert_timezone(self.timestamp, timezone)
    
    @property
    def real_last_edited(self):
        # return self._real_last_edited(self.user.timezone if self.user.timezone else None)
        return self._real_last_edited(None)
    
    def _real_last_edited(self, timezone):
        if not self.last_edited:
            return None
        return convert_timezone(self.last_edited, timezone)
    
    def __repr__(self):
        return '<Post {}>'.format(self.body)
    
@event.listens_for(Post, 'before_update')
def update_post(mapper, connection, target):
    if get_history(target, 'body').has_changes() or\
        get_history(target, 'title').has_changes():
        target.last_edited = func.now()

class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(255))
    votes = db.Column(db.Integer, default=0)
    vote_records = db.relationship('Vote', backref='reply', lazy='dynamic', cascade='all, delete-orphan')
    timestamp = db.Column(db.DateTime, index=True, default=func.now())
    last_edited = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=True)
    accepted = db.Column(db.Boolean, default=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('reply.id', name='fk_reply_parent_id'))
    replies = db.relationship('Reply', backref=db.backref('parent', remote_side=[id]), lazy='dynamic', cascade='all, delete-orphan')

    @property
    def user(self):
        return User.query.get(self.user_id)

    @property
    def real_timestamp(self):
        # return self._real_timestamp(self.user.timezone if self.user.timezone else None)
        return self._real_timestamp(None)
    
    def _real_timestamp(self, timezone):
        if not self.timestamp:
            return None
        return convert_timezone(self.timestamp, timezone)
    
    @property
    def real_last_edited(self):
        # return self._real_last_edited(self.user.timezone if self.user.timezone else None)
        return self._real_last_edited(None)
    
    def _real_last_edited(self, timezone):
        if not self.last_edited:
            return None
        return convert_timezone(self.last_edited, timezone)
    
    def __repr__(self):
        return '<Reply {}>'.format(self.body)

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