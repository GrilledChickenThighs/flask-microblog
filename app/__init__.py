from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

server = Flask(__name__)
server.config.from_object(Config)
db = SQLAlchemy(server)
migrate = Migrate(server, db)

# Login Manager
login = LoginManager(server)
login.login_view = 'login'  # Redirects users to login if they try to view protected page




from app import routes, models, errors

# Set debug to 0 and get email tracebacks error handling in production
if not server.debug:
    # Email notifications
    if server.config['MAIL_SERVER']:
        auth = None
        if server.config['MAIL_USERNAME'] or server.config['MAIL_PASSWORD']:
            auth = (server.config['MAIL_USERNAME'], server.config['MAIL_PASSWORD'])
        secure = None
        if server.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(server.config['MAIL_SERVER'], server.config['MAIL_PORT']),
            fromaddr='no-reply@' + server.config['MAIL_SERVER'],
            toaddrs=server.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        server.logger.addHandler(mail_handler)

        # Log File
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        server.logger.addHandler(file_handler)

        server.logger.setLevel(logging.INFO)
        server.logger.info('Microblog startup')


