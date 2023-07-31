from flask import Flask,request
from extension import db
import os
from flask_marshmallow import Marshmallow
from dbmodels import User,UserInfo,UserType

app= Flask(__name__)

baseurl= os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///'+os.path.join(baseurl,'Demostore.db')
db.init_app(app)
ma = Marshmallow(app)

# Welcome Api
@app.get("/")
def Welcome():
    return "Welcome to flask Api Learning"

import user_controller ,account_controller,userinfo_controller
import commands

if __name__ == "__main__":
    app.run()

