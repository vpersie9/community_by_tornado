#-*-coding:utf-8-*-
__author__ = 'vpersie9'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from model.user import User
from form.auth import LoginForm,RegisterForm,Confirm_register
import tornado.web

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        username=None
        self.render("index.html",username=username)

    def post(self):
        form=self.judgeForm()
        if form.validate() and isinstance(form,LoginForm):
            email=form.email.data
            password=form.password.data
            self.login_operator(email,password)
        elif form.validate() and isinstance(form,RegisterForm):
            username=form.username.data
            email=form.email.data
            password=form.password.data
            password2=form.password2.data
            self.register_operator(username,email,password,password2)


    def login_operator(self,email,password):
        user=User(email=email).search()
        if not user:
            self.write(u"用户不存在")
        elif user.verify_password(password_context=password):
            self.redirect("http://www.baidu.com")
        else:
            self.write(u"邮箱或者密码错误")

    def register_operator(self,username,email,password,password2):
        confirm=Confirm_register()
        if confirm.registered_test(email=email):
            self.write(u"该邮箱已经注册了")
        elif confirm.registered_test(username=username):
            self.write(u"该用户名已经注册了")
        elif not confirm.password_same_test(password,password2):
            self.write(u"前后密码输入不一致")
        elif not confirm.email_css(email):
            self.write(u"请填写正确的邮箱格式 如example@xxx.com")
        else:
            user=User(username=username,email=email,password=password)
            user.save()
            self.redirect("http://www.baidu.com")

    def judgeForm(self):
        items=self.request.arguments
        if set(items.keys()) == {'username', 'password2', 'password', 'email'}:
            return RegisterForm(self.request.arguments)
        if set(items.keys()) == {'password', 'email'}:
            return LoginForm(self.request.arguments)