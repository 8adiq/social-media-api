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
            user_data = request.get_json() 

            user_schema = UserSchema() 

            user = user_schema.load(user_data,session=db.session) 

            hashed_password = generate_password_hash(user.password)

            new_user = User (
                username = user['username'],
                email = user['email'],
                password = hashed_password )

            db.session.add(new_user)
            db.session.commit()

            return jsonify({
                'Message': f'{new_user.username}\'s account has been created.',
                # 'user_id' : new_user.uid
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

            user = User.query.filter_by(username=username).first()

            if not user:
                return jsonify({'Login Error':'User doesn\'t exit. Create an account'}),401
            if not check_password_hash(user.password, password):
                return jsonify({'Login Error':'Username or password incorrect'}),401
            
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
            
            post_data = request.get_json()
            post_content = post_data.get('content_')

            post_schema = PostSchema()

            post = post_schema.load(post_data,session=db.session)

            new_post = Post(
                content_ = post['content_'],
                uid = session['uid']
            )

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
