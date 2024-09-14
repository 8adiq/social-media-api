from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields,validate,ValidationError
from models import User,Post,Like,Comment


# Schemas for each model
class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User

    username = fields.String(required=True,validate=validate.Length(min=1,max=100))
    email = fields.Email(required=True)
    uid = fields.Integer(dump_only=True)
    password = fields.String(required=True,load_only=True)

    # username and password validation here 

class PostSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Post

    content_ = fields.String(required=True,validate=validate.Length(min=1,max=300))
    created_at = fields.DateTime()
    uid = fields.Integer(dump_only=True)
    pid = fields.Integer(dump_only=True) 

    # post content validation here


class LikeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Like

    lid = fields.Integer(dump_only=True)
    uid = fields.Integer(required=True)
    pid = fields.Integer(required=True)