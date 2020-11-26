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

class DFT(db.Model):
    __tablename__ = 'eb_dft'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    Zeolite = db.Column(db.String(16))
    site = db.Column(db.String(16))
    Veff=db.Column(db.Integer)
    PLD = db.Column(db.Float(16))
    RDLS = db.Column(db.Float(16))
    EbDFT = db.Column(db.Float(16))
    EbDFTmax = db.Column(db.Float(16))

class FL_K(db.Model):
    __tablename__ = 'eb_fl_k'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    Zeolite = db.Column(db.String(16))
    Veff=db.Column(db.Integer)
    PLD = db.Column(db.Float(16))
    RDLS = db.Column(db.Float(16))
    EbFLmax = db.Column(db.Float(16))

    def getDataK(self):
        return self.Zeolite,self.Veff,self.PLD,self.RDLS,self.EbFLmax

class FL_UK(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    Zeolite = db.Column(db.String(16))
    Veff=db.Column(db.Integer)
    PLD = db.Column(db.Float(2))
    RDLS = db.Column(db.Float(4))
    EbFLmax = db.Column(db.Float(16))
    def getDataUK(self):
        return self.Veff,self.PLD,self.RDLS,self.EbFLmax
    def checkDataUK(self,rdls_input,pld_input):
        return (self.RDLS==rdls_input and self.PLD==pld_input)
'''
if __name__ == "__main__":
    db.drop_all()
    db.create_all()
'''
