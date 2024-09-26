from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields,validates,ValidationError,validate,post_load
from models import User,Post,Comment
from flask import jsonify
import re

# Schemas for each model
class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User

    username = fields.String(required=True,validate=validate.Length(min=3,max=100))
    email = fields.Email(required=True)
    uid = fields.Integer(dump_only=True)
    password = fields.String(required=True,load_only=True,validate=validate.Length(min=6))

    # creating a model instance after loading from json
    @post_load
    def make_user(self,data,**kwargs):
        """"""
        return User(**data)

    # Validation 
    @validates('username')
    def validate_username(self,value):
        """validating username"""
        if any(char in value for char in " !@#$%^&*()"):
            raise ValidationError('Username should not contain spaces or special characters')
        
    @validates('email')
    def validate_email(self,value):
        """checking for existing email"""
        existing_user = User.query.filter_by(email=value).first()
        if existing_user:
            raise ValidationError(' An account with this email already exists. Login instead.')
        
    @validates('password')
    def validate_password(self,value):
        """ validating password"""

        if not all([
            re.search(r'[A-Z]', value),
            re.search(r'[a-z]',value),
            re.search(r'[!@#$%^&*()]',value),
            re.search(r'[0-9]',value)
        ]):
            raise ValidationError('Password much contain a number, an uppercase letter, a lowercase letter and a special character')

class PostSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Post

    text = fields.String(required=False,validate=validate.Length(min=1,max=300))
    picture = fields.List(fields.Url(),required=False)
    video = fields.List(fields.Url(),required=False)
    created_at = fields.DateTime()
    uid = fields.Integer(dump_only=True)
    pid = fields.Integer(dump_only=True) 


class CommentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Comment
    content_ = fields.String(required=True,validate=validate.Length(min=1,max=300))
    cid = fields.Integer(dump_only=True)
    uid = fields.Integer(dum_only=True)
    pid = fields.Integer(required=True)


