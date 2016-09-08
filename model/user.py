#-*-coding:utf-8-*
__author__ = 'vpersie9'

u"""
后续工作安装sqlalchemy-migrate 进行数据库的迁移
"""

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from config import Config
from sqlalchemy import create_engine
from sqlalchemy import Column,Integer,String,Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash,check_password_hash

engine=create_engine(Config.SQLALCHEMY_URI,echo=True)
DBsession=sessionmaker(bind=engine)
session=DBsession()
Model=declarative_base()

class CreateDelete(object):
    def init_db(self):
        Model.metadata.create_all(engine)

    def drop_db(self):
        Model.metadata.drop_all(engine)

class Permission(object):
    FOLLOW=0x01
    COMMENT=0x02
    WRITE_ARTICLES=0x04
    MODERATE_COMMENTS=0x08
    ADMINISTER=0x80

class Role(Model):
    __tablename__="roles"
    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String(64),unique=True)
    default=Column(Boolean,default=True,index=True)
    permissions=Column(Integer)

    @staticmethod
    def insert_roles():
        roles=dict(
            User=(Permission.FOLLOW|Permission.COMMENT|
                  Permission.WRITE_ARTICLES,True),
            Moderater=(Permission.FOLLOW|Permission.COMMENT|
                       Permission.WRITE_ARTICLES|
                       Permission.MODERATE_COMMENTS,False),
            Administrater=(0xff,False)
        )
        for item in roles:
            role=session.query(Role).filter_by(name=item).first()
            if role == None:
                role=Role(name=item)
            role.permissions=roles[item][0]
            role.default=roles[item][1]
            session.add(role)
        session.commit()

    def query_all(self):
        all=session.query(Role.name).all()
        return all

class User(Model):
    __tablename__="users"
    id=Column(Integer,primary_key=True)
    email=Column(String(64),unique=True,index=True)
    username=Column(String(64),unique=True,index=True)
    password_hash=Column(String(128))

    def __init__(self,**kwargs):
        super(User,self).__init__(**kwargs)

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self,password_content):
        self.password_hash=generate_password_hash(password_content)

    def verify_password(self,password_context):
        return check_password_hash(self.password_hash,password_context)

    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception,e:
            session.rollback()
            return e

    @staticmethod
    def search(**kwargs):
        try:
            return session.query(User).filter_by(**kwargs).first()
        except Exception,e:
            return e
