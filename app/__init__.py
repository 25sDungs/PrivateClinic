from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote

# from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = '!@#$%^&casASD1675S56a4sd49w7c1zx04acSD2G'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/phongmachtudb' % quote('P@ssw0rd')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app=app)


# login = LoginManager(app)
