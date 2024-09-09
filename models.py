from app import db
from sqlalchemy.sql import func

class User(db.Model):
    __tablename__ = 'Users'
    uid = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(100), nullable = False)
    password_hash = db.Column(db.String(100), nullable = False)

    # relationships
    posts = db.relationship('Post',backref='user',lazy='select')
    likes = db.relationship('Like', backref='user', lazy='select')
    comments = db.relationship('Comment',backref='user',lazy='select')

class Post(db.Model):
    __tablename__ = 'Posts'
    pid = db.Column(db.Integer, primary_key = True)
    content_ = db.Column(db.Text, nullable = False)
    uid = db.Column(db.Integer, db.ForeignKey('Users.uid'), nullable = False)
    created_at = db.Column(db.DateTime, default=func.now())

    # relationships
    user = db.relationship('User',backref='posts',lazy='select')
    likes = db.relationship('Like', backref='post', lazy='select')
    comments =db.relationship('Comment',backref='post',lazy='select')

class Like(db.Model):
    __tablename__ = 'Likes'
    lid = db.Column(db.Integer, primary_key = True)
    uid = db.Column(db.Integer, db.ForeignKey('Users.uid'), nullable = False)
    pid = db.Column(db.Integer, db.ForeignKey('Posts.pid'), nullable = False)

    # relationships
    user = db.relationship('User',backref='likes',lazy='select')
    post = db.relationship('Post',backref='likes',lazy='select')

class Comment(db.Model):
    __tablename__ = 'Comments'
    cid = db.Column(db.Integer, primary_key = True)
    content_ = db.Column(db.Text, nullable = False)
    uid = db.Column(db.Integer, db.ForeignKey('Users.uid'), nullable = False)
    pid = db.Column(db.Integer, db.ForeignKey('Posts.pid'), nullable = False)
    created_at = db.Column(db.DateTime, default=func.now())

    # relationships
    user = db.relationship('User', backref='comments', lazy='select')
    post = db.relationship('Post',backref='comments',lazy='select')



    



