from extension import db
from app import app

@app.cli.command('db_create')
def db_create():
    db.create_all()
    print("table created")

# @app.cli.command('do_seed')
# def do_seed():

#     #Add user types

#     usertypes=[UserType(type='Admin'),UserType(type='User'),UserType(type='Sales'),UserType(type='Employee')]
#     for i in usertypes:
#         db.session.add(i)
        
#     #Add user details

#     user1=User(username='Anandk',password='Anndyklnt@010',email="anandk@mailator.com",usertypeid=1)
#     user2=User(username='dipuk',password='dipuk@010',email='dipukbarh@mailator.com',usertypeid=2)

#     # Add UserInfo

#     userinfo1= UserInfo(firstname='Anand', lastname='Kumar',userid=1)
#     userinfo2= UserInfo(firstname='Dipu', lastname='Kumar',userid=2)

#     db.session.add_all([userinfo1,user1,user2,userinfo2])
#     # db.session.add_all([ad minn,user,sale,employee])
#     db.session.commit()

#     print("data seeded")

@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print("table dropped")
