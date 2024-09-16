from flask import jsonify,request,session
from sqlalchemy.exc import SQLAlchemyError
from models import User,Post,Comment,Like
from serializer import UserSchema,PostSchema,LikeSchema
from marshmallow import ValidationError
from utils import allowed_file,upload_gallary



def all_routes(app,db):
    @app.route('/register',methods=['POST'])
    def register():
        """creating a new user"""
        try:

            user_data = request.get_json()
            print(user_data) 

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

        if 'uid' not in session:
            return jsonify({'Error':'You need to login first '}),401
        
        text = request.form.get('text')
        file = request.files.get('file')

        if not file and not text:
            return jsonify({'Error':'At least text or file is required'}),401
        
        if file:
        
                file = request.files['file']

                if file.filename == '':
                    return jsonify({'Uploading error':"No file selected for your post"}),400

                if allowed_file(file):
                    try:
                        gallary_url = upload_gallary(file)
                    except Exception as e:
                        return jsonify({'Error':str({e})}),501
                else:
                    return jsonify({'Error':'Invalid valid'}),401
                
        else:
            gallary_url = None
        
        new_post = Post(
            text= request.form.get('text',''),
            uid=session['uid'],
            gallary = gallary_url

        )
        db.session.add(new_post)
        db.session.commit()
        return jsonify({"Message":"Posted successfully"}),201
        

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
        
    @app.route('/posts/<int:pid>/like',methods=['POST'])
    def like_post(pid):
        """liking a post"""
        try:
            if  not pid or 'uid' not in session:
                return jsonify({'Error':'You need to be logged in and select a post.'}),400
            
            if session.get('uid') and pid :
                user_id = session.get('uid')

                liked = Like.query.filter_by(uid=user_id,pid=pid).first()

                if liked:
                    return jsonify({'Message':"You have already liked this post"}),200
                
                new_like = Like(uid=user_id,pid=pid)

                db.session.add(new_like)
                db.session.commit()
                return jsonify({'Message':'Post liked'}),200

        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'SQL Error':str({e})}),500
        
    @app.route('/posts/<int:pid>/comment',methods=['POST'])
    def comment(pid):
        """commenting on a post"""

        try:
            if  not pid or 'uid' not in session:
                return jsonify({'Error':'You need to be logged in and select a post.'}),400
            
            if session.get('uid') and pid:
                user_id = session.get('uid')
                commented = Comment.query.filter_by(uid=user_id,pid=pid).first()

            if commented:
                return jsonify({'Message':'You have already commented on this post'}),200
            data = request.get_json()
            comment_text = data.get('content_')
            new_comment = Comment(content_=comment_text,uid=user_id,pid=pid)
            db.session.add(new_comment)
            db.session.commit()
            return jsonify({'Message':'Commented'})

        except Exception as e:
            db.session.rollback()
            return jsonify({'Error':str({e})})
            

