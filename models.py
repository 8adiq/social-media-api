from app import db
from sqlalchemy.sql import func
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields,validate,ValidationError

class User(db.Model):
    __tablename__ = 'Users'
    uid = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False)
    password = db.Column(db.String(255), nullable = False)

    # relationships
    posts = db.relationship('Post',backref='author',lazy='select')
    likes = db.relationship('Like', backref='liker', lazy='select')
    comments = db.relationship('Comment',backref='commenter',lazy='select')

class Post(db.Model):
    __tablename__ = 'Posts'
    pid = db.Column(db.Integer, primary_key = True)
    content_ = db.Column(db.Text, nullable = False)
    uid = db.Column(db.Integer, db.ForeignKey('Users.uid'), nullable = False)
    created_at = db.Column(db.DateTime, default=func.now())

    # relationships
    # author = db.relationship('User',backref='posts',lazy='select')
    likes = db.relationship('Like', backref='liked_post', lazy='select')
    comments =db.relationship('Comment',backref='commented_post',lazy='select')

class Like(db.Model):
    __tablename__ = 'Likes'
    lid = db.Column(db.Integer, primary_key = True)
    uid = db.Column(db.Integer, db.ForeignKey('Users.uid'), nullable = False)
    pid = db.Column(db.Integer, db.ForeignKey('Posts.pid'), nullable = False)

    # relationships
    user = db.relationship('User',backref='user_likes',lazy='select')
    post = db.relationship('Post',backref='post_likes',lazy='select')

class Comment(db.Model):
    __tablename__ = 'Comments'
    cid = db.Column(db.Integer, primary_key = True)
    content_ = db.Column(db.Text, nullable = False)
    uid = db.Column(db.Integer, db.ForeignKey('Users.uid'), nullable = False)
    pid = db.Column(db.Integer, db.ForeignKey('Posts.pid'), nullable = False)
    created_at = db.Column(db.DateTime, default=func.now())

    # relationships
    user = db.relationship('User', backref='user_comments', lazy='select')
    post = db.relationship('Post',backref='post_comments',lazy='select')


# Schemas for each model
class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

    username = fields.String(required=True,validate=validate.Length(min=1,max=100))
    email = fields.Email(required=True)
    uid = fields.Integer(dump_only=True)
    password = fields.String(required=True,load_only=True)

class PostSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        load_instance = True

    content_ = fields.String(required=True,validate=validate.Length(min=1,max=300))
    created_at = fields.DateTime()
    uid = fields.Integer(required=True)
    pid = fields.Integer(dump_only=True) 


class LikeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Like

    lid = fields.Integer(dump_only=True)
    uid = fields.Integer(required=True)
    pid = fields.Integer(required=True)





