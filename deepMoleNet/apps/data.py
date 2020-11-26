from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from apps import app
from flask_login import UserMixin

db = SQLAlchemy(app)

class Info(db.Model,UserMixin):
    __tablename__ = 'user_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(16))
    email = db.Column(db.String(255),unique=True)
    password = db.Column(db.String(16))
    addtime = db.Column(db.DATETIME,index=True,default=datetime.now)
    license = db.Column(db.Integer, default=0)

    #def __repr__(self):
       # return '<user %r>' %self.username

    def check_pwd(self,password):
        return self.password == password

    def check_license(self):
        return self.license != 0
    def get_username(self):
        return self.username

# if __name__ == '__main__':
#     db.drop_all()
#     db.create_all()