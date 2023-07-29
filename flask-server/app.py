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

import user_controller 
import commands

# @app.post("/store")
# def savestore():
#     data=request.get_json()
#     new_store={"name":data['name'],"items":[]}
#     stores.append(new_store)
#     return stores,201
    

# @app.get("/store/<string:name>/getitem")
# def getitemsbystore(name):
#     for store in stores:
#         if store['name']==name:
#             return store['items']
#     return {'message':'store not found'},404

# @app.post("/store/<string:name>")
# def saveitemsbystore(name):
#     request_data=request.get_json()
#     for store in stores:
#         if store['name']==name:
#             new_item={"item":request_data['item'],"price":request_data['price']}
#             store['items'].append(new_item)
#             return stores,201
#     return {'message':'store not found'},404


if __name__ == "__main__":
    app.run()

