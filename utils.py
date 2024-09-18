import cloudinary
from cloudinary.utils import cloudinary_url
import cloudinary.uploader
import os,uuid
from dotenv import load_dotenv
from flask import jsonify
from serializer import PostSchema,CommentSchema,UserSchema

load_dotenv()

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'mp4', 'avi'}

cloudinary.config(
    cloud_name = os.getenv('cloud_name'),
    api_key = os.getenv('cloud_api_key'),
    api_secret = os.getenv("cloud_api_secret"),
    secure = True
)

def upload_gallary(file):
    upload_result = cloudinary.uploader.upload(file,public_id=str(uuid.uuid4()))
    return upload_result['secure_url']

    
def allowed_file(file):
    filename = file.filename
    if not filename:
        return False
    extension = filename.rsplit('.',1)[1].lower() if '.' in filename else None
    return extension in ALLOWED_EXTENSIONS if extension else None

