from flask import jsonify,request,session
from sqlalchemy.exc import SQLAlchemyError
from models import User,UserSchema,Post,PostSchema,LikeSchema,Comment
from werkzeug.security import generate_password_hash,check_password_hash
from marshmallow import ValidationError


def all_routes(app,db):
    @app.route('/register',methods=['POST'])
    def register():
        """creating a new user"""
        try:
            user_data = request.get_json() # loading data from body

            if not any([
                user_data.get('username'),
                user_data.get('email'),
                user_data.get('password')
            ]):
                return jsonify({'Error': 'All fields must be filled.'})

            user_schema = UserSchema() # creating an instance of the userschema

            # validating the data passed and loading it intothe model data
            user = user_schema.load(user_data,session=db.session) 

            hashed_password = generate_password_hash(user.password) # generatig a hash for the password

            # creating a new user
            new_user = User (
                username = user.username,
                email = user.email,
                password = hashed_password )

            # adding the new user to the sessio and commiting to the database
            db.session.add(new_user)
            db.session.commit()

            # Success message
            return jsonify({
                'Message': f'{new_user.username}\'s account has been created.',
                'user_id' : new_user.uid
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

            # retrieving login data from body
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')

            user = User.query.filter_by(username=username).first() # getting user from database

            # checking if user exits and if the password matches
            if user and check_password_hash(user.password,password):

                session['uid'] = user.uid  # storing user id in a session

                return jsonify({'Message': 'Logged in successfully'}),200
            else:
                return jsonify({'Error': 'Invalid Credentials'}),401
            
        except Exception as e:

            return jsonify({'Error':str({e})})
                  

    @app.route('/post',methods=['POST'])
    def post():
        """creating a new post by a logged in user"""

        try:
            if 'uid' not in session:
                return jsonify({'Error':'You need to login first '})
            
            post_data = request.get_json() # getting post data

            post_schema = PostSchema()

            # validate and deserialize input data
            post = post_schema.load(post_data,session=db.session)

            user_id = session['uid'] # getting uid from the session

            # creating new post and connecting it to the uid in the session
            new_post = Post(
                content_ = post.content_,
                uid = user_id
            )

            # adding new post to the data and commiting
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
        

    @app.route('/all_posts')
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