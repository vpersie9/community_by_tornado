#-*-coding:utf-8-
__author__ = 'vpersie9'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import re
from model.user import User
from wtforms import StringField,PasswordField,SubmitField
from wtforms_tornado import Form

class LoginForm(Form):
    email=StringField("email")
    password=PasswordField("password")
    submit=SubmitField("submit")

class RegisterForm(Form):
    username=StringField("username")
    email=StringField("email")
    password=PasswordField("password")
    password2=PasswordField("password2")

class Confirm_register(object):
    def registered_test(self,**kwargs):
        return User.search(**kwargs)

    def password_same_test(self,passwd,passwd2):
        return passwd==passwd2

    def email_css(self,email):
        return bool(len(email)>7) and re.match(
            "^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email)
