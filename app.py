from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)

db = SQLAlchemy()


def create_app():

        app.config['SQLALCHEMY_DATABASE_URI']  = f'postgresql://{os.getenv("user")}:{os.getenv("password")}@{os.getenv("host")}:{os.getenv("port")}/{os.getenv("dbname")}'
        
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


        db.init_app(app)


        # routes
        from routes import all_routes
        all_routes(app,db)

        migrate = Migrate()

        return app