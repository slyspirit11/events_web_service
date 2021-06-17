import os
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS

from os import path

from werkzeug.security import generate_password_hash

db = SQLAlchemy()
DB_NAME = 'EventsDB'


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SECRET_KEY'] = os.urandom(16)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:512163@localhost/{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    # app.config['MAIL_PORT'] = 587
    # app.config['MAIL_USE_TLS'] = True
    # app.config['MAIL_USERNAME'] = 'batt098@gmail.com'
    # app.config['MAIL_DEFAULT_SENDER'] = '"EventsApp" <noreply@example.com>'
    db.init_app(app)
    # migrate = Migrate(app, db)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    create_database(app)

    from .models import User

    login_manager = LoginManager()
    login_manager.login_view = 'auth.sign_in'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('backend/' + DB_NAME):
        db.create_all(app=app)
        print('Database created successfully!!')

def create_admin():
    from .models import User, Role
    if not User.query.filter(User.email == 'batt098@gmail.com').first():
        user = User(
            username='emperor',
            email='batt098@gmail.com',
            email_confirmed_at=datetime.utcnow(),
            password=generate_password_hash('512163')
        )
        user.roles.append(Role.query.filter(Role.name == 'Admin').first())
        db.session.add(user)
        db.session.commit()