from flask import jsonify,request,session
from sqlalchemy.exc import SQLAlchemyError
from models import User,Post,Comment,Like,Blacklist
from serializer import UserSchema,PostSchema,CommentSchema
from marshmallow import ValidationError
from utils import allowed_file,upload_gallary
from flask_jwt_extended import create_access_token,jwt_required, get_jwt_identity



def all_routes(app,db):
    @app.route('/register',methods=['POST'])
    def register():
        """creating a new user"""
        try:

            user_data = request.get_json() # getting JSON data from request body

            # using schema to validate and deserialize the inout data
            user_schema = UserSchema() 
            user = user_schema.load(user_data,session=db.session)
            
            user.set_password(user.password) #hashing password before saving to db
            
            # adding user to session and commiting changes to the db
            db.session.add(user)
            db.session.commit()

            return jsonify({
                'Message': f'{user.username}\'s account has been created.',
                }),201
            
        except ValidationError as err:
            return jsonify({'Validation Error': err.messages}),400
        
        except SQLAlchemyError as e:
            db.session.rollback() # rollback session incase of a db error
            return jsonify({'Error': str({e})}),500

    @app.route('/login', methods=['POST'])
    def login():
        """Authenticating a user before making a post"""
        try:
            # extracting login data from request
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')

            # Authenticatiing the login data provided 
            user = User.authenticate(username,password)
            if not user:
                return jsonify({'Login Error':'Username or password is incorrect'}),401
            
            # creating a JWT access token for the authenticated user
            access_token = create_access_token(identity=user.uid)
            return jsonify({'Message':'User logged in.',
                            'access-token': access_token
                            }),200        
        except Exception as e:
            return jsonify({'Error':str({e})}),501
                  

    @app.route('/posts',methods=['GET','POST'])
    @jwt_required() # ensuing user is authenticated
    def post():
        """creating a new post by a logged in user"""

        # Extracting current user id from access token and checking if the user is blacklisted ie logged out
        user_id = get_jwt_identity()
        blacklisted = Blacklist.query.filter_by(acc_key=str(user_id)).first()

        if request.method == 'POST':
            # creating a new post

            if  blacklisted or not user_id :
                return jsonify({'Error':'You need to login first '}),401
            
            # Extracting text and file from request
            text = request.form.get('text')
            file = request.files.get('file')

            if not file and not text:
                return jsonify({'Error':'At least text or file is required'}),400
            
            # Uploading file to cloudinary
            if file:
                    file = request.files['file']
                    if file.filename == '':
                        return jsonify({'Uploading error':"No file selected for your post"}),400

                    if allowed_file(file): # checking if file type is allowed
                        try:
                            gallary_url = upload_gallary(file) # uploading file and storing url
                        except Exception as e:
                            return jsonify({'Error':str({e})}),501
                    else:
                        return jsonify({'Error':'Invalid file type'}),400
            else:
                gallary_url = None

            # creating new post object
            new_post = Post(
                text= request.form.get('text',''),
                uid=user_id,
                gallary = gallary_url
            )

            # adding post to session and commiting to db
            db.session.add(new_post)
            db.session.commit()
            return jsonify({"Message":"Posted successfully"}),201
        
        elif request.method == 'GET':
            # getting all posts
            try:
            
                if  blacklisted or not user_id :
                    return jsonify({'Error':'You need to login first '}),401

                # Quering all posts from database
                posts = Post.query.all()
                if not posts:
                    return jsonify({'Message':'No posts to show'}),204
                
                # Serializing posts data
                post_shema = PostSchema(many=True)
                all_posts = post_shema.dump(posts)

                return jsonify({
                    'Message':'All retrieved successfully',
                    'Post': all_posts
                })
            except ValidationError as err:
                return jsonify({'Validation Error': err.messages}),401
            
            except SQLAlchemyError as e:
                return jsonify({'Error': str({e})}),500

    @app.route('/posts/<int:pid>/like',methods=['POST','GET'])
    @jwt_required() # ensuing user is authenticated
    def like_post(pid):
        """liking a post"""
        # Extracting current user id from access token and checking if the user is blacklisted ie logged out
        user_id = get_jwt_identity()
        blacklisted = Blacklist.query.filter_by(acc_key=str(user_id)).first()

        if request.method == 'POST':
            try:
                if  blacklisted or not pid or not user_id:
                    return jsonify({'Error':'You need to be logged in and select a post.'}),401
                
                if user_id and pid :
                    
                    # checking if user has already liked the post
                    liked = Like.query.filter_by(uid=user_id,pid=pid).first()

                    if liked:
                        return jsonify({'Message':"You have already liked this post"}),200
                    
                    new_like = Like(uid=user_id,pid=pid) #creating new like record

                    # adding new like to session and commiting to the database
                    db.session.add(new_like)
                    db.session.commit()
                    return jsonify({'Message':'Post liked'}),201

            except SQLAlchemyError as e:
                db.session.rollback()
                return jsonify({'SQL Error':str({e})}),500
            
        elif request.method == 'GET':
            # retrieving all likes for a post
            if blacklisted or not user_id:
                return jsonify({"Message":"you need to log in first"}),401
            
            # couting the number of likes a post has
            number_of_likes = Like.query.filter_by(pid=pid).count()
            if not number_of_likes:
                return jsonify({'Message':'No Likes'}),204

            return jsonify({'Message':f'{number_of_likes} likes on this post'})
        
    @app.route('/posts/<int:pid>/comment',methods=['POST','GET'])
    @jwt_required()
    def comment(pid):
        """commenting on a post"""

        # Extracting current user id from access token and checking if the user is blacklisted ie logged out
        user_id = get_jwt_identity()
        blacklisted = Blacklist.query.filter_by(acc_key=str(user_id)).first()

        if request.method == 'POST':
            try:
                if  blacklisted or not pid or not user_id:
                    return jsonify({'Message':'You need to be logged in and select a post to comment on.'}),401
                
                # checking if the user has already liked the post
                if user_id and pid:
                    commented = Comment.query.filter_by(uid=user_id,pid=pid).first()

                if commented:
                    return jsonify({'Message':'You have already commented on this post'}),200
                
                # extracting the comment content from the request data
                data = request.get_json()
                comment_text = data.get('content_')

                # creating a new comment for the post
                new_comment = Comment(content_=comment_text,uid=user_id,pid=pid)
                
                db.session.add(new_comment)
                db.session.commit()
                return jsonify({'Message':'Comment made'}),201
            
            except ValidationError as err:
                return jsonify({'Validation Error':err.messages})
            
            except Exception as e:
                db.session.rollback()
                return jsonify({'Error':str({e})}),500
            
        elif request.method == 'GET':
            # Retrieving all comments for a post
            if blacklisted or not user_id:
                return jsonify({'Message':'You need to login first.'}),401
            
            # Querying comments for the post
            comments = Comment.query.filter_by(pid=pid).all()
            if not comments:
                return jsonify({'Message':'No comments'}),204

             # Serializing the comments data
            comment_schema = CommentSchema(many=True)
            serialized_comments = comment_schema.dump(comments)

            return jsonify({'Message':'Comments retrived',
                            'Comments': serialized_comments
                                })
    
    @app.route('/logout', methods=['POST'])
    @jwt_required()
    def logout():
        """logging out"""
        # extracting current user id from access token
        user_id = get_jwt_identity()

        # blacklisting the user to prevent access
        blacklist = Blacklist(user_id)
        db.session.add(blacklist)
        db.session.commit()

        return jsonify('Message','You\'ve logged out successfully'),204
