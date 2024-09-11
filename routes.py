from flask import jsonify,request
from sqlalchemy.exc import SQLAlchemyError
from models import User,UserSchema,Post,PostSchema,LikeSchema,Comment
from werkzeug.security import generate_password_hash
from marshmallow import ValidationError


def all_routes(app,db):
    @app.route('/register',methods=['POST'])
    def register():
        """creating a new user"""
        try:
            user_data = request.get_json() # loading data from body

            user_schema = UserSchema() # creating an instance of the userschema

            user = user_schema.load(user_data,session=db.session) # loading and validating the passsed data

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
        

    @app.route('/post',methods=['POST'])
    def post():
        """creating a new post"""

        try:
            post_data = request.get_json()

            post_schema = PostSchema()

            post = post_schema.load(post_data,session=db.session)

            db.session.add(post)
            db.session.commit()

            return jsonify({
                'Message': 'Post successfully created',
                'Post': post_schema.dump(post)}),201
        
        except ValidationError as err:
            return jsonify({'Validation Error': err.messages}),400
        
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'Error':str({e})}),500
        

    @app.route('/all_posts')
    def get_all_posts():
        """getting all posts"""

        try:
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