from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__) #__name__ is __main__
app.config['SECRET_KEY'] ='38f63965b699a92c103454bfe63a4e96'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
app.config['SERVER_NAME']='llocalhost.localdomain:5000'



from flask_login import LoginManager
login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'

from PaymentApplication import routes








