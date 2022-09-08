from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_web():
    web = Flask(__name__)
    web.config['SECRET_KEY'] = 'Ou Yeah buddy let us go YeahBOOOOI ou lets gooooo'
    web.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(web)


    
    from .views import views
    from .auth import auth

    web.register_blueprint(views, url_prefix='/')
    web.register_blueprint(auth, url_prefix='/') 

    from .models import User, Flag


    create_database(web)

    login_manager = LoginManager()
    login_manager.login_manager = 'auth.login'
    login_manager.init_app(web)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return web 

def create_database(web):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=web)
        print('Database created!')