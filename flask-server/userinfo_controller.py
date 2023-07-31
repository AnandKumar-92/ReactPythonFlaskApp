import json
from model_schema.users import user_schema,users_schema
from base_response import BaseResponse
from flask import request,send_file
from dbmodels import UserInfo
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
from app import app
from extension import db
import os

@app.get("/user/get_avatar/<userid>")
def GetAvatar(userid):
    base_responses=BaseResponse()
    userinfo=UserInfo.query.filter_by(id=userid).first()
    if userinfo:
        print(userinfo)
        if userinfo.Avatar_url.strip() =="" or userinfo.Avatar_url.strip() is None:
            base_responses.isSuccess=False
            base_responses.ErrorMessage="Profile picture not found"
            return json.dumps(base_responses.__dict__),404
        else:
            root_dir = os.path.dirname(app.instance_path)
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
    




