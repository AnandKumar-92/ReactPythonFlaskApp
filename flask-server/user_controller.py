from app import app,ma
from dbmodels import User,UserInfo,UserType
from flask import jsonify,request
from extension import db
import re
from sqlalchemy.exc import IntegrityError


@app.get("/user")
def GetUsers():
    user_list=User.query.all()
    result= users_schema.dump(user_list)
    return jsonify(result),200

def checkusername(username):
    if username.strip() =="" or username is None:        
        return {'Error Message':"username is empty"}
    else:
        isexituser=User.query.filter_by(username=username).first()
        if isexituser:
            return {'Error Message':"Username is already exist"}
    return {}

@app.post("/user/signup")
def SignupUser():
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
        return jsonify(ErrorMessage),400
    else:
        new_user=User(username=usern,password=passwd,email=emailid,usertypeid=2)
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            return jsonify({"errormessage":"User already exist"}),409
    
        return jsonify(message="Successfully saved"),201

@app.get("/user/<int:userid>")
def Getuserbyid(userid):
    user=User.query.filter_by(id=userid).first()
    if user:
        return jsonify(user_schema.dump(user))
    else:
        return {"Error Massage":"User Not found"},404

@app.put("/user/update")
def UpdateUser():
    passwd=request.form['password']
    userid=request.form['user_id']
    emailid=request.form['email']
    ErrorMessage=[]

    if emailid.strip() !="" and emailid is not None:
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if not re.fullmatch(regex, emailid) :
            ErrorMessage.append({'Error Message':"Email is not valid"})
    
    if len(ErrorMessage)>0:
        return jsonify(ErrorMessage),400
    else:
        user=User.query.filter_by(id=userid).first()
        if user:
            user.email=emailid if emailid.strip() !="" and emailid is not None else user.email
            user.password= passwd if  passwd.strip() !="" and passwd is not None else user.password
            db.session.commit()
            return jsonify(message=f"{user.username} has updated"),202
        else:
            return jsonify(Errormessage="User not found"),404

@app.delete("/user/delete/<int:userid>")
def DeleteUser(userid):
    user=User.query.filter_by(id=userid).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify(Message="Deleted Successfully"),202
    else:
        return {"Error Massage":"User Not found"},404




class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
         fields = ('id','username', 'password', 'email','count')

user_schema = UserSchema()
users_schema = UserSchema(many=True)