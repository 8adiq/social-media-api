from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_restx import Api


load_dotenv()
db = SQLAlchemy()

def create_app():
        app = Flask(__name__)
        api = Api(app,
                  doc='/swagger',
                  title='Social Media Api',
                  version='1.0',
                  description='This Social Media API built with Flask that allows users to register, log in, create posts, like posts, and comment on them. JWT authentication is used to manage user sessions, and the API supports file uploads (e.g., images ) for posts. Additionally, users can log out by blacklisting their JWT tokens.',
                  authorizations={
                          'Bearer Auth':{
                                  'type':'apiKey',
                                  'in':'header',
                                  'name':'Authorization',
                                  'description':'Add "Bearer <your_token>" to the Authorization header'
                          }
                  }) 
        app.config['SQLALCHEMY_DATABASE_URI']  = os.getenv("DATABASE_URL")
        # f'postgresql://{os.getenv("user")}:{os.getenv("password")}@{os.getenv("host")}:{os.getenv("port")}/{os.getenv("dbname")}'
        
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        app.config['JWT_SECRET_KEY'] = os.getenv('secret_key')
        app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)  # Token expires in 1 hour

        db.init_app(app)

        jwt = JWTManager(app)

        from doc_model import ns
        api.add_namespace(ns)
        # routes
        from routes import all_routes
        all_routes(app,db)



        migrate = Migrate(app,db)

        return app