import json
from model_schema.users import user_schema,users_schema
from base_response import BaseResponse
from flask import request
from dbmodels import User
import jwt
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime,timedelta
from app import app
from extension import db
from sqlalchemy.exc import IntegrityError
import re

@app.post("/user/signup")
def SignupUser():
    base_responses=BaseResponse()
    usern=request.form['username']
    passwd=request.form['password']
    emailid=request.form['email']
    role=request.form['role']
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
        hashed_password=generate_password_hash(passwd,method='sha256')
        new_user=User(username=usern,password=hashed_password,email=emailid,usertypeid=2,role=role)
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            base_responses.isSuccess=False
            base_responses.ErrorMessage="User already exist"
            return json.dumps(base_responses.__dict__),409
        base_responses.isSuccess=True
        base_responses.ErrorMessage="Sign up completed"
        return json.dumps(base_responses.__dict__),201


@app.post("/login")
def GetLoginDetails():
    base_responses=BaseResponse()
    username= request.form['username']
    password=request.form['password']
    user=User.query.filter_by(username=username).first()
    if user:
        hash_pwd=check_password_hash(user.password,password)
        if hash_pwd:
            base_responses.isSuccess=True
            cur_time=datetime.now()+ timedelta(minutes=15)
            epoc_time=cur_time.timestamp()
            data={
                "payload":user_schema.dump(user),
                "exp":int(epoc_time)
            }
            jwt_token=jwt.encode(data,"AnandKumar010",algorithm="HS256")
            base_responses.data={"Token":jwt_token}
            return json.dumps(base_responses.__dict__),200
        else:
            base_responses.isSuccess=False
            base_responses.ErrorMessage="Invalid password"
            return json.dumps(base_responses.__dict__),200
    else:
        base_responses.isSuccess=False
        base_responses.ErrorMessage="Invalid user"
        return json.dumps(base_responses.__dict__),200
    
def checkusername(username):
    if username.strip() =="" or username is None:        
        return {'Error Message':"username is empty"}
    else:
        isexituser=User.query.filter_by(username=username).first()
        if isexituser:
            return {'Error Message':"Username is already exist"}
    return {}