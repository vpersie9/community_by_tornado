#-*-coding:utf-8
__author__ = 'vpersie9'

u'''
分析tornado源码 为tornado配置jinja2模板语言
重写了部分tornado.template.BaseLoader的继承方法
进行简单的封装,并没有重写tornado.web.RequestHandler的
self.render_string 和 self.render方法，
简单实现了jinja2模板语言的配置。
'''

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import threading
import tornado.template
import tornado.web
import jinja2

class RTemplate(object):
    def __init__(self,template_instance):
        self.template_instance=template_instance

    def generate(self,**kwargs):
        return self.template_instance.render(**kwargs)

class JinjaLoader(tornado.template.BaseLoader):
    def __init__(self,root_directory,**kwargs):
        self.root=os.path.abspath(root_directory)
        self.jinja_env=jinja2.Environment(loader=jinja2.FileSystemLoader(self.root),**kwargs)
        self.templates={}
        self.lock=threading.RLock()

    def resolve_path(self, name, parent_path=None):
        return name

    def _create_template(self, name):
        template_instance=RTemplate(self.jinja_env.get_template(name))
        return template_instance