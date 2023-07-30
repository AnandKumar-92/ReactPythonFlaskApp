from sqlalchemy import Column,Integer,String
from app import db

class UserInfo(db.Model):
    __tablename__="userinfo"
    id=Column(Integer,primary_key=True)
    firstname=Column(String(50))
    lastname=Column(String(50))
    userid=Column(Integer)
    userid=Column(db.ForeignKey('users.id'))
    user=db.relationship('User',back_populates='userinfo')

class User(db.Model):
    __tablename__="users"
    id=Column(Integer,primary_key=True)
    username=Column(String(50),unique=True,nullable=False)
    password=Column(String(50))
    email=Column(String(50))
    usertypeid=Column(db.ForeignKey('usertype.id'))
    usertype=db.relationship('UserType',back_populates='user')
    userinfo=db.relationship('UserInfo',back_populates='user')

class UserType(db.Model):
    __tablename__="usertype"
    id=Column(Integer,primary_key=True)
    type=Column(String(50),unique=True,nullable=False)
    user=db.relationship('User',back_populates='usertype')



