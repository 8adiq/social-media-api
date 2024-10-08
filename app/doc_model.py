from flask_restx import Namespace, Resource, fields


ns = Namespace('social',description='Social Media Api Operation')

# Define request/response models for documentation
register_model = ns.model('RegisterUser', { 
    'username':fields.String(required=True, description='username of the user'),
    'email':fields.String(required=True, description='Email of the user'),
    'password':fields.String(required=True, description='Password of the user')
})

login_model = ns.model('LoginUser', { 
    'username':fields.String(required=True, description='username of the user'),
    'password':fields.String(required=True, description='Password of the userr')
})

# would be passed as a form data
post_model = ns.model('Post',{
    'text': fields.String(description='Text content of the post', required=False),
    'file': fields.Raw(description='Name of the file to be uploaded', required=False)
})

comment_model = ns.model('Comment',{
    'content_':fields.String(required=True, description='Comment content')
})


like_model = ns.model('Like', {
    'pid': fields.Integer(description='Post ID')
})