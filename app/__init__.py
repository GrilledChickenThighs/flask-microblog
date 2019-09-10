from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

server = Flask(__name__)
server.config.from_object(Config)
db = SQLAlchemy(server)
migrate = Migrate(server, db)

# Login Manager
login = LoginManager(server)
login.login_view = 'login'  # Redirects users to login if they try to view protected page




from app import routes, models