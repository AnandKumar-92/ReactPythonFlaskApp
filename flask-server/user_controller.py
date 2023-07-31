from app import app
from dbmodels import User,UserInfo,UserType
from flask import request,send_file
from extension import db
import re
from sqlalchemy.exc import IntegrityError
from base_response import BaseResponse
import json
from sqlalchemy import text,create_engine
from marshmallow import Schema, fields
import os
from sqlalchemy.orm import sessionmaker
from datetime import datetime

baseurl= os.path.abspath(os.path.dirname(__file__))
engine = create_engine('sqlite:///'+os.path.join(baseurl,'Demostore.db'))
Session = sessionmaker(bind=engine)
session = Session()

@app.get("/user/get_avatar/<userid>")
def GetAvatar(userid):
    base_responses=BaseResponse()
    userinfo=UserInfo.query.filter_by(id=userid).first()
    if userinfo:
        if userinfo.Avatar_url.strip() =="" or userinfo.Avatar_url.strip() is None:
            base_responses.isSuccess=False
            base_responses.ErrorMessage="Profile picture not found"
            return json.dumps(base_responses.__dict__),404
        else:
            root_dir = os.path.dirname(app.instance_path)
            print(root_dir)
            print(f"{root_dir}\{userinfo.Avatar_url}")
            return send_file(f"{root_dir}\{userinfo.Avatar_url}")
    else:
        base_responses.isSuccess=False
        base_responses.ErrorMessage="User not found"
        return json.dumps(base_responses.__dict__),404

@app.put("/user/update_avatar/<userid>")
def UpdateAvatar(userid):
    base_responses=BaseResponse()
    file=request.files['avatar']
    new_file=str(datetime.now().timestamp()).replace('.','')
    split_file=file.filename.split('.')
    ext=split_file[len(split_file)-1]
    avaterpath=f"avatar\{new_file}.{ext}"
    file.save(avaterpath)
    userinfo=UserInfo.query.filter_by(id=userid).first()
    if userinfo:
        userinfo.Avatar_url=avaterpath
        db.session.commit()
        base_responses.isSuccess=True
        base_responses.message=f" {avaterpath} Photo uploaded successfully"
        return json.dumps(base_responses.__dict__),202
    else:
        base_responses.isSuccess=False
        base_responses.ErrorMessage="User not found"
        return json.dumps(base_responses.__dict__),404

    return "success"

#Get All User with details
@app.get("/user/pagination")
def GetUserspagination():
    page = request.args.get('page',1,int)
    per_page=request.args.get('per_page',1,int)
    base_responses=BaseResponse()
    user_list=User.query.paginate(page=page, per_page=per_page,error_out=False).items

    if user_list:
        base_responses.isSuccess=True
        base_responses.data={"count": len(user_list), "users":users_schema.dumps(user_list)} 
        return  json.dumps(base_responses.__dict__),200
    else:
        base_responses.isSuccess=False
        base_responses.ErrorMessage=f"user not found"
        return json.dumps(base_responses.__dict__),200


# #Get All User with details
@app.get("/user")
def GetUsers():

    base_responses=BaseResponse()
    user_list=User.query.all()
    if user_list:
        base_responses.isSuccess=True
        base_responses.data={"count": len(user_list), "users":users_schema.dumps(user_list)} 
        return  json.dumps(base_responses.__dict__),200
    else:
        base_responses.isSuccess=False
        base_responses.ErrorMessage=f"user not found"
        return json.dumps(base_responses.__dict__),404


# User Signup

@app.post("/user/signup")
def SignupUser():
    base_responses=BaseResponse()
    usern=request.form['username']
    passwd=request.form['password']
    emailid=request.form['email']
    ErrorMessage=[]

    checkuser=checkusername(usern)
    if len(checkuser)>0:
        ErrorMessage.append(checkuser)

    if passwd.strip() =="" or passwd is None:
        ErrorMessage.append({'Error Message':"Password is empty"})
    
    if emailid.strip() =="" or emailid is None:
        ErrorMessage.append({'Error Message':"Email is empty"})
    else:
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if not re.fullmatch(regex, emailid) :
            ErrorMessage.append({'Error Message':"Email is not valid"})
    
    if len(ErrorMessage)>0:
        base_responses.isSuccess=False
        base_responses.ErrorMessage=json.dumps(ErrorMessage)
        return json.dumps(base_responses.__dict__),400
    else:
        new_user=User(username=usern,password=passwd,email=emailid,usertypeid=2)
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            base_responses.isSuccess=False
            base_responses.ErrorMessage="User already exist"
            return json.dumps(base_responses.__dict__),409
        base_responses.isSuccess=True
        base_responses.ErrorMessage="Successfully saved"
        return json.dumps(base_responses.__dict__),201

# get user by id
@app.get("/user/<int:userid>")
def Getuserbyid(userid):
    base_responses=BaseResponse()
    user=User.query.filter_by(id=userid).first()
    if user:
        print(user_schema.dumps(user))
        base_responses.isSuccess=True
        base_responses.data= user_schema.dumps(user)
        return json.dumps(base_responses.__dict__),200
    else:
        base_responses.isSuccess=False
        base_responses.ErrorMessage=f"{userid} not found"
        return json.dumps(base_responses.__dict__),404

@app.put("/user/update")
def UpdateUser():
    base_responses=BaseResponse()

    passwd=request.form['password']
    userid=request.form['user_id']
    emailid=request.form['email']
    ErrorMessage=[]

    if emailid.strip() !="" and emailid is not None:
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if not re.fullmatch(regex, emailid) :
            ErrorMessage.append({'Error Message':"Email is not valid"})
    
    if len(ErrorMessage)>0:
        base_responses.isSuccess=False
        base_responses.ErrorMessage=json.dumps(ErrorMessage)
        return json.dumps(base_responses.__dict__),400
    else:
        user=User.query.filter_by(id=userid).first()
        if user:
            user.email=emailid if emailid.strip() !="" and emailid is not None else user.email
            user.password= passwd if  passwd.strip() !="" and passwd is not None else user.password
            db.session.commit()
            base_responses.isSuccess=True
            base_responses.message=f"{user.username} has updated"
            return json.dumps(base_responses.__dict__),202
        else:
            base_responses.isSuccess=False
            base_responses.ErrorMessage="User not found"
            return json.dumps(base_responses.__dict__),404

@app.delete("/user/delete/<int:userid>")
def DeleteUser(userid):
    base_responses=BaseResponse()
    user=User.query.filter_by(id=userid).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        base_responses.isSuccess=True
        base_responses.message="Successfully deleted"
        return json.dumps(base_responses.__dict__),201
    else:
        base_responses.isSuccess=False
        base_responses.ErrorMessage="User not found"
        return json.dumps(base_responses.__dict__),404


def checkusername(username):
    if username.strip() =="" or username is None:        
        return {'Error Message':"username is empty"}
    else:
        isexituser=User.query.filter_by(username=username).first()
        if isexituser:
            return {'Error Message':"Username is already exist"}
    return {}

# Schema
class UserSchema(Schema):
    id = fields.Str()
    username = fields.Str()
    email = fields.Str()


user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Schema
class UserInfoSchema(Schema):
    id = fields.Str()
    firstname = fields.Str()
    lastname = fields.Str()
    Avatar_url = fields.Str()


userinfo_schema = UserInfoSchema()
usersinfo_schema = UserInfoSchema(many=True)
