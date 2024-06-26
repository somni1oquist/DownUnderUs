from sqlalchemy import UniqueConstraint, func, event
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, loginManager
from sqlalchemy.orm.attributes import get_history
from .tools import convert_timezone, user_level

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    suburb = db.Column(db.String(50))
    profile_image = db.Column(db.String(255))
    posts = db.relationship('Post', back_populates='user', lazy='dynamic', cascade='all, delete-orphan')
    replies = db.relationship('Reply', back_populates='user', lazy='dynamic', cascade='all, delete-orphan')
    interested_topics = db.Column(db.String(200))
    points = db.Column(db.Integer, default=0,nullable=False)
    registered_date = db.Column(db.DateTime, index=True, default=func.now())
    titles = db.relationship('Title', backref='user', lazy='dynamic')

    @property
    def level(self):
        return user_level(self.id)
    
    @hybrid_property
    def title_names(self):
        return [title.title for title in self.titles]

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
    replies = db.relationship('Reply',
                              back_populates='post',
                              lazy='dynamic',
                              cascade='all, delete-orphan',
                              order_by='Reply.timestamp')
    topic = db.Column(db.String(100), nullable=False)
    tags = db.Column(db.String(200))
    location = db.Column(db.String(100))
    user = db.relationship(User, back_populates='posts')

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
    user = db.relationship(User, back_populates='replies')
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=True)
    post = db.relationship(Post, back_populates='replies')
    accepted = db.Column(db.Boolean, default=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('reply.id', name='fk_reply_parent_id'))
    replies = db.relationship('Reply',
                              backref=db.backref('parent', remote_side=[id]),
                              lazy='dynamic', cascade='all, delete-orphan',
                              order_by='Reply.timestamp')

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

class Title(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    awarded_date = db.Column(db.DateTime, index=True, default=func.now())

class Points(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=func.now())
    points_added = db.Column(db.Integer, nullable=False)

    user = db.relationship('User', backref='points_history')

    def __repr__(self):
        return f"<Points {self.user_id}: +{self.points_added} at {self.timestamp}>"
