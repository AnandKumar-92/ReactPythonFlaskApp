from flask_sqlalchemy import SQLAlchemy
from flask import request
from base_response import BaseResponse
import json,re,jwt
from functools import wraps

db=SQLAlchemy()

#decorator to auth token
def auth_token(*argss,**kwargs):
    def inner1(func):
        @wraps(func)
        def inner2(*args):
            base_responses=BaseResponse()
            authorization=request.headers.get("Authorization")
            if authorization is None:
                base_responses.isSuccess=False
                base_responses.data="Please enter token"
                return json.dumps(base_responses.__dict__),400
            if re.match("^Bearer *([^ ]+) *$", authorization, flags=0):
                token=authorization.split(" ")[1]
                try:
                    data=jwt.decode(token,"AnandKumar010",algorithms="HS256")
                    print(len(argss))
                    if len(argss)==0 and len(kwargs)==0:
                        return func(*args)
                    else :
                        if data['payload']['role']==kwargs['Role']:
                            return func(*args)
                        else:
                            base_responses.isSuccess=False
                            base_responses.data="Unauthorize Access"
                            return json.dumps(base_responses.__dict__),401
                except Exception as e:
                    base_responses.isSuccess=False
                    if str(e)=="Signature has expired":
                        base_responses.data="Token has expired"
                    else:
                        base_responses.data=str(e)
                    return json.dumps(base_responses.__dict__),401
            else:
                base_responses.isSuccess=False
                base_responses.data="Invalid Token"
                return json.dumps(base_responses.__dict__),401
        return inner2
    return inner1

         