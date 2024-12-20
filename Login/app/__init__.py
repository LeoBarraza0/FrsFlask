import os 
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from flask_bootstrap import Bootstrap 
from flask_login import LoginManager 
from flask_bcrypt import Bcrypt 
from flask_cors import CORS


db = SQLAlchemy() 
bootstrap = Bootstrap() 
bcrypt = Bcrypt() 
login_manager = LoginManager() 
login_manager.login_view = "authentication.log_in_user" 
login_manager.session_protection = "strong" 

def create_app(config_type): 
    app = Flask(__name__) 
    configuration = os.path.join(os.getcwd(), "Login", "config", config_type + ".py") 
    app.config.from_pyfile(configuration) 
    db.init_app(app) 
    bootstrap.init_app(app) 
    login_manager.init_app(app)
    bcrypt.init_app(app) 
    CORS(app)  # Habilitar CORS para todas las rutas
    from Login.app.auth import authentication 
    app.register_blueprint(authentication) 
    return app