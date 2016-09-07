#-*-coding:utf-8-
__author__ = 'vpersie9'

u"""
项目或者脚本的相关介绍...
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os.path
import tornado.options
import tornado.web
import tornado.httpserver
import tornado.ioloop

from tornado.options import define,options
define("port",default=8070,help="run on the given port",type=int)

class Application(tornado.web.Application):
    def __init__(self):

        handlers=[(r"/",MainHandler)]

        settings=dict(
            debug=True,
            template_path=os.path.join(os.path.dirname(__file__),"templates"),
            static_path=os.path.join(os.path.dirname(__file__),"static"),
            xsrf_cookies=True,
            cookie_secret="",
            autoescape=None,
        )
        tornado.web.Application.__init__(self,handlers,**settings)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        username=u"曾翔"
        self.render("index.html",username=username)

def main():
    tornado.options.parse_command_line()
    http_server=tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__=="__main__":
    main()
