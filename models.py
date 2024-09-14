from app import db
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash,check_password_hash


class User(db.Model):
    __tablename__ = 'Users'
    uid = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False)
    password = db.Column(db.String(255), nullable = False)

    def __repr__(self) -> str:
        return f'User: {self.username}, Email: {self.email}'
    
    def set_password(self,password):
        self.password = generate_password_hash(password)
        
    def check_password(self,password):
        return check_password_hash(self.password,password)
    
    def authenticate(username,password):
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user
        return None



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
    likes = db.relationship('Like', backref='liked_post', lazy='select')
    comments =db.relationship('Comment',backref='commented_post',lazy='select')

    def __repr__(self):
        return f'Post: {self.content_}, posted at {self.created_at}'

class Like(db.Model):
    __tablename__ = 'Likes'
    lid = db.Column(db.Integer, primary_key = True)
    uid = db.Column(db.Integer, db.ForeignKey('Users.uid'), nullable = False)
    pid = db.Column(db.Integer, db.ForeignKey('Posts.pid'), nullable = False)

class Comment(db.Model):
    __tablename__ = 'Comments'
    cid = db.Column(db.Integer, primary_key = True)
    content_ = db.Column(db.Text, nullable = False)
    uid = db.Column(db.Integer, db.ForeignKey('Users.uid'), nullable = False)
    pid = db.Column(db.Integer, db.ForeignKey('Posts.pid'), nullable = False)
    created_at = db.Column(db.DateTime, default=func.now())







