import cloudinary
from cloudinary.utils import cloudinary_url
import cloudinary.uploader
import os,uuid
from dotenv import load_dotenv

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
    if filename and '.' in filename:
        parts = filename.rsplit('.', 1)
        if len(parts) == 2:
            extension = parts[1].lower()
            if extension in ALLOWED_EXTENSIONS:
                return True
        else:
            print("Filename does not have a valid extension part.")
    else:
        print("Filename does not contain a dot or is empty.")
    