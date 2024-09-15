from flask import jsonify
import boto3
import os
from dotenv import load_dotenv

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'mp4', 'avi'}

def allowed_file(filename):
    if '.' in filename:
        extention = filename.rsplit('.',1)[1].lower()
        if extention in ALLOWED_EXTENSIONS:
            return True
    else:
        return False
    
# creating a client to connect with aws
s3 = boto3.client(
                's3',
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                region_name=os.getenv('AWS_REGION')
        )