from flask import jsonify,request,session
from sqlalchemy.exc import SQLAlchemyError
from models import User,Post,Comment
from serializer import UserSchema,PostSchema,LikeSchema
from marshmallow import ValidationError
from werkzeug.utils import secure_filename
from utils import allowed_file,s3
import os



def all_routes(app,db):
    @app.route('/register',methods=['POST'])
    def register():
        """creating a new user"""
        try:
            user_data = request.get_json() 

            user_schema = UserSchema() 

            user = user_schema.load(user_data,session=db.session) 
            
            user.set_password(user.password) #hashing password 

            db.session.add(user)
            db.session.commit()

            return jsonify({
                'Message': f'{user.username}\'s account has been created.',
                }),201
        
        except ValidationError as err:
            return jsonify({'Validation Error': err.messages})
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'Error': str({e})})

    @app.route('/login', methods=['POST'])
    def login():
        """Authenticating a user before making a post"""
        try:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')

            user = User.authenticate(username,password)

            if not user:
                return jsonify({'Login Error':'Username or password is incorrect'}),401
            
            session['uid'] = user.uid
            return jsonify({'Message':'User logged in.'}),200        

        except Exception as e:
            return jsonify({'Error':str({e})})
                  

    @app.route('/create_post',methods=['POST'])
    def post():
        """creating a new post by a logged in user"""

        try:
            if 'uid' not in session:
                return jsonify({'Error':'You need to login first '})
            
            if 'file' not in request.files:
                post_data = request.get_json()

                post_schema = PostSchema(only=('text','created_at'))

                post = post_schema.load(post_data,session=db.session)

                new_post = Post(
                    text = post['text'],
                    uid = session['uid']
                )
            else:
                S3_BUCKET = os.getenv('S3_BUCKET_NAME')
                file = request.files['file']
                if file.filename == '':
                    return jsonify({'Uploading error':"No file selected for your post"})
                if file and allowed_file(file):
                    filename = secure_filename(file.filename)
                    try:
                        s3.uplaod_fileobj(
                            file,filename,S3_BUCKET,
                            ExtraArgs={
                                "ACL":"Public-read",
                                "ContentType":file.content_type
                            }
                        )
                        return jsonify({"Mesage":"Post made"})
                    except Exception as e:
                        return jsonify({"Error":str({e})})

            db.session.add(new_post)
            db.session.commit()

            return jsonify({
                'Message': 'Post successfully created',
                'Post': post_schema.dump(new_post)}),201
        
        except ValidationError as err:
            return jsonify({'Validation Error': err.messages}),400
        
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'Error':str({e})}),500
        

    @app.route('/get_all_posts')
    def get_all_posts():
        """getting all posts"""

        try:

            if 'uid' not in session:
                return jsonify({'Error':'You need to login first '})

            posts = Post.query.all()

            post_shema = PostSchema(many=True)

            all_posts = post_shema.dump(posts)

            return jsonify({
                'Message':'All retrieved successfully',
                'Post': all_posts
            })
        except ValidationError as err:
            return jsonify({'Validation Error': err.messages})
        except SQLAlchemyError as e:
            return jsonify({'Error': str({e})})
        
    @app.route('/posts/<int:id>/like',methods=['POST'])
    def like_post():
        """liking a post"""

        try:
            if  'uid' or 'pid' not in session:
                return jsonify({'Error':'You need to be logged in and select a post.'})
            
            # liking logic

        except ValidationError as err:
            return jsonify({'Validation Error': err.messages})
        except SQLAlchemyError as e:
            return jsonify({'SQL Error':str({e})})
