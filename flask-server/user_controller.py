from app import app
from dbmodels import User
from flask import request,send_file
from extension import db,auth_token
from base_response import BaseResponse
import json,os,re
from sqlalchemy import text,create_engine
from sqlalchemy.orm import sessionmaker
from model_schema.users import user_schema,users_schema
from logging_extn import logger

baseurl= os.path.abspath(os.path.dirname(__file__))
engine = create_engine('sqlite:///'+os.path.join(baseurl,'Demostore.db'))
Session = sessionmaker(bind=engine)
session = Session()

#Get All User with details
@app.get("/user/pagination")
def GetUserspagination():
    logger.info(f" {__name__} started")
    page = request.args.get('page',1,int)
    per_page=request.args.get('per_page',1,int)
    base_responses=BaseResponse()
    user_list=User.query.paginate(page=page, per_page=per_page,error_out=False).items

    if user_list:
        base_responses.isSuccess=True
        base_responses.data={"count": len(user_list), "users":users_schema.dumps(user_list)} 
        logger.info(f"Pagination response for page={page} and per_page={per_page}:{users_schema.dumps(user_list)}" )
        return  json.dumps(base_responses.__dict__),200
    else:
        base_responses.isSuccess=False
        base_responses.ErrorMessage=f"No Record Found"
        logger.info(f"Pagination response for page={page} and per_page={per_page}: No Record Found " )

        return json.dumps(base_responses.__dict__),200


# #Get All User with details
@app.get("/user")
@auth_token(Role="User", City="Bihar")
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
 