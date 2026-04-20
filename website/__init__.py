import torch
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from ml.model_loader import load_model

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'super-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['TEMP_UPLOAD_FOLDER'] = 'temp_uploads'
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

    os.makedirs(
        os.path.join(app.root_path, app.config['TEMP_UPLOAD_FOLDER']),
        exist_ok=True
    )

    db.init_app(app)

    # Load ML model once
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model, threshold, preprocessing = load_model(device)

    app.config["MODEL"] = model
    app.config["DEVICE"] = device
    app.config["THRESHOLD"] = threshold
    app.config["PREPROCESSING"] = preprocessing

    from .views import views
    from .auth import auth

    app.register_blueprint(views)
    app.register_blueprint(auth)

    from .models import User
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
