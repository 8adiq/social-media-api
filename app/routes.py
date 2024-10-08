from flask import jsonify,request,session
from sqlalchemy.exc import SQLAlchemyError
from models import User,Post,Comment,Like,Blacklist
from serializer import UserSchema,PostSchema,CommentSchema
from marshmallow import ValidationError
from utils import allowed_file,upload_gallary
from flask_jwt_extended import create_access_token,jwt_required, get_jwt_identity
from doc_model import register_model,ns,login_model,post_model,like_model,comment_model
from flask_restx import Resource



def all_routes(app,db):
    # @app.route('/register',methods=['POST'])
    # def register():
    #     """creating a new user"""
    #     try:

    #         user_data = request.get_json() # getting JSON data from request body

    #         # using schema to validate and deserialize the inout data
    #         user_schema = UserSchema() 
    #         user = user_schema.load(user_data,session=db.session)
            
    #         user.set_password(user.password) #hashing password before saving to db
            
    #         # adding user to session and commiting changes to the db
    #         db.session.add(user)
    #         db.session.commit()

    #         return jsonify({
    #             'Message': f'{user.username}\'s account has been created.',
    #             }),201
            
    #     except ValidationError as err:
    #         return jsonify({'Validation Error': err.messages}),400
        
    #     except SQLAlchemyError as e:
    #         db.session.rollback() # rollback session incase of a db error
    #         return jsonify({'Error': str({e})}),500

    # @app.route('/login', methods=['POST'])
    # def login():
    #     """Authenticating a user before making a post"""
    #     try:
    #         # extracting login data from request
    #         data = request.get_json()
    #         username = data.get('username')
    #         password = data.get('password')

    #         # Authenticatiing the login data provided 
    #         user = User.authenticate(username,password)
    #         if not user:
    #             return jsonify({'Login Error':'Username or password is incorrect'}),401
            
    #         # creating a JWT access token for the authenticated user
    #         access_token = create_access_token(identity=user.uid)
    #         return jsonify({'Message':'User logged in.',
    #                         'access-token': access_token
    #                         }),200        
    #     except Exception as e:
    #         return jsonify({'Error':str({e})}),501

                
    # @app.route('/posts',methods=['GET','POST'])
    # @jwt_required() # ensuing user is authenticated
    # def post():
    #     """creating a new post by a logged in user"""

    #     # Extracting current user id from access token and checking if the user is blacklisted ie logged out
    #     user_id = get_jwt_identity()
    #     blacklisted = Blacklist.query.filter_by(acc_key=str(user_id)).first()

    #     if request.method == 'POST':
    #         # creating a new post

    #         if  blacklisted or not user_id :
    #             return jsonify({'Error':'You need to login first '}),401
            
    #         # Extracting text and file from request
    #         text = request.form.get('text')
    #         file = request.files.get('file')

    #         if not file and not text:
    #             return jsonify({'Error':'At least text or file is required'}),400
            
    #         # Uploading file to cloudinary
    #         if file:
    #                 file = request.files['file']
    #                 if file.filename == '':
    #                     return jsonify({'Uploading error':"No file selected for your post"}),400

    #                 if allowed_file(file): # checking if file type is allowed
    #                     try:
    #                         gallary_url = upload_gallary(file) # uploading file and storing url
    #                     except Exception as e:
    #                         return jsonify({'Error':str({e})}),501
    #                 else:
    #                     return jsonify({'Error':'Invalid file type'}),400
    #         else:
    #             gallary_url = None

    #         # creating new post object
    #         new_post = Post(
    #             text= request.form.get('text',''),
    #             uid=user_id,
    #             gallary = gallary_url
    #         )

    #         # adding post to session and commiting to db
    #         db.session.add(new_post)
    #         db.session.commit()
    #         return jsonify({"Message":"Posted successfully"}),201
        
    #     elif request.method == 'GET':
    #         # getting all posts
    #         try:
            
    #             if  blacklisted or not user_id :
    #                 return jsonify({'Error':'You need to login first '}),401

    #             # Quering all posts from database
    #             posts = Post.query.all()
    #             if not posts:
    #                 return jsonify({'Message':'No posts to show'}),204
                
    #             # Serializing posts data
    #             post_shema = PostSchema(many=True)
    #             all_posts = post_shema.dump(posts)

    #             return jsonify({
    #                 'Message':'All retrieved successfully',
    #                 'Post': all_posts
    #             })
    #         except ValidationError as err:
    #             return jsonify({'Validation Error': err.messages}),401
            
    #         except SQLAlchemyError as e:
    #             return jsonify({'Error': str({e})}),500

        # @app.route('/posts/<int:pid>/like',methods=['POST','GET'])
    # @jwt_required() # ensuing user is authenticated
    # def like_post(pid):
    #     """liking a post"""
    #     # Extracting current user id from access token and checking if the user is blacklisted ie logged out
    #     user_id = get_jwt_identity()
    #     blacklisted = Blacklist.query.filter_by(acc_key=str(user_id)).first()

    #     if request.method == 'POST':
    #         try:
    #             if  blacklisted or not pid or not user_id:
    #                 return jsonify({'Error':'You need to be logged in and select a post.'}),401
                
    #             if user_id and pid :
                    
    #                 # checking if user has already liked the post
    #                 liked = Like.query.filter_by(uid=user_id,pid=pid).first()

    #                 if liked:
    #                     return jsonify({'Message':"You have already liked this post"}),200
                    
    #                 new_like = Like(uid=user_id,pid=pid) #creating new like record

    #                 # adding new like to session and commiting to the database
    #                 db.session.add(new_like)
    #                 db.session.commit()
    #                 return jsonify({'Message':'Post liked'}),201

    #         except SQLAlchemyError as e:
    #             db.session.rollback()
    #             return jsonify({'SQL Error':str({e})}),500
            
    #     elif request.method == 'GET':
    #         # retrieving all likes for a post
    #         if blacklisted or not user_id:
    #             return jsonify({"Message":"you need to log in first"}),401
            
    #         # couting the number of likes a post has
    #         number_of_likes = Like.query.filter_by(pid=pid).count()
    #         if not number_of_likes:
    #             return jsonify({'Message':'No Likes'}),204

    #         return jsonify({'Message':f'{number_of_likes} likes on this post'})

      # @app.route('/posts/<int:pid>/comment',methods=['POST','GET'])
    # @jwt_required()
    # def comment(pid):
    #     """commenting on a post"""

    #     # Extracting current user id from access token and checking if the user is blacklisted ie logged out
    #     user_id = get_jwt_identity()
    #     blacklisted = Blacklist.query.filter_by(acc_key=str(user_id)).first()

    #     if request.method == 'POST':
    #         try:
    #             if  blacklisted or not pid or not user_id:
    #                 return jsonify({'Message':'You need to be logged in and select a post to comment on.'}),401
                
    #             # checking if the user has already liked the post
    #             if user_id and pid:
    #                 commented = Comment.query.filter_by(uid=user_id,pid=pid).first()

    #             if commented:
    #                 return jsonify({'Message':'You have already commented on this post'}),200
                
    #             # extracting the comment content from the request data
    #             data = request.get_json()
    #             comment_text = data.get('content_')

    #             # creating a new comment for the post
    #             new_comment = Comment(content_=comment_text,uid=user_id,pid=pid)
                
    #             db.session.add(new_comment)
    #             db.session.commit()
    #             return jsonify({'Message':'Comment made'}),201
            
    #         except ValidationError as err:
    #             return jsonify({'Validation Error':err.messages})
            
    #         except Exception as e:
    #             db.session.rollback()
    #             return jsonify({'Error':str({e})}),500
            
    #     elif request.method == 'GET':
    #         # Retrieving all comments for a post
    #         if blacklisted or not user_id:
    #             return jsonify({'Message':'You need to login first.'}),401
            
    #         # Querying comments for the post
    #         comments = Comment.query.filter_by(pid=pid).all()
    #         if not comments:
    #             return jsonify({'Message':'No comments'}),204

    #          # Serializing the comments data
    #         comment_schema = CommentSchema(many=True)
    #         serialized_comments = comment_schema.dump(comments)

    #         return jsonify({'Message':'Comments retrived',
    #                         'Comments': serialized_comments
    #                             })
    @ns.route('/register')
    class RegisterResource(Resource):
        @ns.expect(register_model) # connecting the route to the register_model
        def post(self):
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

                return {
                    'Message': f'{user.username}\'s account has been created.',
                    },201
                
            except ValidationError as err:
                return {'Validation Error': err.messages},400
            
            except SQLAlchemyError as e:
                db.session.rollback() # rollback session incase of a db error
                return {'Error': str({e})},500
    
    @ns.route('/login')
    class LoginResource(Resource):
        @ns.expect(login_model)
        def post(self):
            try:
                data = request.get_json()
                username = data.get('username')
                password = data.get('password')

                user = User.authenticate(username,password)

                if not user:
                    return {'Login Error':'Username or password incorrect'},401
                
                access_token = create_access_token(identity=user.uid)
                return {'Message':'User logged in','access-token':access_token},200
            
            except (SQLAlchemyError,Exception) as e:
                db.session.rollback()
                return {'Error':str({e})},501
            
    @ns.route('/post')
    class PostResource(Resource):
        @ns.expect(post_model)
        @jwt_required()
        @ns.doc(security='Bearer Auth')
        def post(self):
            try:
                user_id = get_jwt_identity()
                blacklisted = Blacklist.query.filter_by(acc_key=str(user_id)).first()

                if blacklisted or not user_id:
                    return {'Error':'You need to log in first'},401
                
                text = request.form.get('text')
                file = request.files.get('file')

                # text = app.api.payload['text']
                # file = app.api.payload.get('file')

                if not file and not text:
                    return {'Error':'At least text or a file is required'},400
                
                if file:
                    if file.filename == '':
                     return {'Uploading error':"No file selected for your post"},400
                    
                    if allowed_file(file):
                        try :
                            gallery_url = upload_gallary(file)
                        except Exception as e:
                            return {'Error':str({e})},501
                    else:
                        return {'Message':'Invalid file type'},400
                gallery_url =None

                new_post = Post(
                text= request.form.get('text',''),
                uid=user_id,
                gallery = gallery_url
                )

                db.session.add(new_post)
                db.session.commit()
                return {'Message':'Post made'},201

            except (SQLAlchemyError,Exception) as e:
                db.session.rollback()
                return {'Error':str({e})},500
            
        @jwt_required()
        @ns.doc(security='Bearer Auth')
        def get(self):
            user_id = get_jwt_identity()
            blacklisted = Blacklist.query.filter_by(acc_key=str(user_id)).first()
            try:
                if blacklisted or not user_id:
                    return {'Error':'You need to log in first'},401
                
                posts = Post.query.all()

                if not posts:
                    return {'Message':'No posts to show'}
                
                post_schema = PostSchema(many=True)
                all_posts = post_schema.dump(posts)

                return {'Message':'All post retrieved','Posts':all_posts}
            
            except ValidationError as e:
                return {'Error': e.messages}
            
            except SQLAlchemyError as err:
                db.session.rollback()
                return {'Error':str({err})}
            
    @ns.route('/posts/<int:pid>/like')
    class LikeResource(Resource):
        @ns.expect(like_model)
        @jwt_required()
        @ns.doc(security='Bearer Auth')
        def post(self,pid):
            try:
                user_id = get_jwt_identity()
                blacklisted = Blacklist.query.filter_by(acc_key=str(user_id)).first()

                if blacklisted or not user_id:
                    return {'Message':'You need to login first'},401
                
                if user_id and pid:

                    liked = Like.query.filter_by(uid=user_id,pid=pid).first()

                    if liked:
                        return {'Message':'You\'ve already liked this post'}
                    
                    new_like = Like(uid=user_id,pid=pid)

                    db.session.add(new_like)
                    db.session.commit()

            except (SQLAlchemyError,Exception) as e:
                db.session.rollback()
                return {'Error':str({e})},501
        
        @jwt_required()
        @ns.doc(security='Bearer Auth')
        def get(self,pid):
            user_id = get_jwt_identity()
            blacklisted = Blacklist.query.filter_by(acc_key=str(user_id)).first()

            try:
                if blacklisted or not user_id:
                    return {'Message':'You need to login first'},401
                
                number_of_likes = Like.query.filter_by(pid=pid).count()

                if not number_of_likes:
                    return {'Message':'No likes'},204
                
                return {'Message':f'{number_of_likes} Likes'}
            
            except (SQLAlchemyError,Exception) as e:
                db.session.rollback()
                return {'Error':str({e})}
        
    @ns.route('/posts/<int:pid>/comments')
    class CommentResource(Resource):
        @ns.expect(comment_model)
        @jwt_required()
        @ns.doc(security='Bearer Auth')
        def post(self,pid):
            user_id = get_jwt_identity()
            blacklisted = Blacklist.query.filter_by(acc_key=str(user_id)).first()

            try:
                if blacklisted or not user_id:
                    return {'Message':'You need to login first.'},401
                
                data = request.get_json()
                content = data.get('content_')

                new_comment = Comment(uid=user_id,pid=pid, content_=content)

                db.session.add(new_comment)
                db.session.commit()
                return {'Message':'Comment made'},201
            
            except ValidationError as err:
                return {'Validation Error':err.messages}
            
            except SQLAlchemyError as e:
                db.session.rollback()
                return {'Error':str({e})}

        @jwt_required()
        @ns.doc(security='Bearer Auth')
        def get(self,pid):
            user_id = get_jwt_identity()
            blacklisted = Blacklist.query.filter_by(acc_key=str(user_id)).first()

            try:
                if blacklisted or not user_id:
                    return {'Message':'You need to login first.'},401
                
                comments = Comment.query.filter_by(pid=pid).all()

                if not comments:
                    return {'Message':'No comments'},204
                
                comment_shema = CommentSchema(many=True)

                serialized_comments = comment_shema.dump(comments)

                return {'Message':'All comments','Comments': serialized_comments}
            
            except (SQLAlchemyError,Exception) as e:
                db.session.rollback()
                return {'Error':str({e})}
            
    
    # @app.route('/logout', methods=['POST'])
    # @jwt_required()
    # def logout():
    #     """logging out"""
    #     # extracting current user id from access token
    #     user_id = get_jwt_identity()

    #     # blacklisting the user to prevent access
    #     blacklist = Blacklist(user_id)
    #     db.session.add(blacklist)
    #     db.session.commit()

    #     return jsonify('Message','You\'ve logged out successfully'),204
