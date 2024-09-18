from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from datetime import timedelta


load_dotenv()
db = SQLAlchemy()

def create_app():
        app = Flask(__name__)

        app.config['SQLALCHEMY_DATABASE_URI']  = f'postgresql://{os.getenv("user")}:{os.getenv("password")}@{os.getenv("host")}:{os.getenv("port")}/{os.getenv("dbname")}'
        
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        app.config['JWT_SECRET_KEY'] = os.getenv('secret_key')
        app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)  # Token expires in 1 hour

        db.init_app(app)

        jwt = JWTManager(app)

        # routes
        from routes import all_routes
        all_routes(app,db)

        migrate = Migrate(app,db)

        return app