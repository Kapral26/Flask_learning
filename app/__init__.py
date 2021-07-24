# -*- coding: utf-8 -*-

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view="login"


if not app.debug:
    if app.config["MAIL_SERVER"]:
        auth = None
        if app.config["MAIL_USERNAME"] and app.config["MAIL_PASSWORD"]:
            auth = (app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"])
        secur = None
        if app.config["MAIL_USE_TLS"]:
            secur = ()

        mail_handler = SMTPHandler(mailhost=(app.config["MAIL_SERVER"], app.config["MAIL_PORT"]),
                                   fromaddr=f"microblog@{app.config['MAIL_SERVER']}",
                                   toaddrs=app.config["ADMINS"],
                                   subject="Microblog Failure",
                                   credentials=auth,
                                   secure=secur
                                   )

        mail_handler.setLevel(logging.ERROR)
        # TODO хуй хнает почему не рабботает
        # app.logger.addHandler(mail_handler)

    if not os.path.exists("logs"):
        os.mkdir("logs")
    file_handler = RotatingFileHandler("logs/microblog.log",
                                       maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.ERROR)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')
else:
    print(f"Debug status:{app.debug}")

from app import routes, models#, errors

