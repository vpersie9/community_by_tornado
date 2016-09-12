#-*-coding:utf-8-
__author__ = 'vpersie9'

u'''
python scrapy 登录豆瓣 并抓取豆瓣精选链接

中间会涉及到验证码问题

我的思路是 遇到验证码 将验证码图片抓取到 然后 手动输入验证码内容 完成登录

辅助函数 考虑使用携程进行调用 提高IO效率

'''

from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.http.cookies import CookieJar
from scrapy.http import FormRequest
import urllib2

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class MainSpider(CrawlSpider):
    name="douban"
    start_urls=['https://accounts.douban.com/login','https://www.douban.com/people/114180036/']
    cookie_file="cookie.txt"

    headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip,deflate",
            "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
            "Connection": "keep-alive",
            "Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent":"Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93",
            "Referer": "http://www.douban.com/"
            }

    post_data={
            'source':'index_nav',
            'redir':'https://www.douban.com/',
            'form_email':'834538028@qq.com',
            'form_password':'jing521jing',
            'captcha-solution':'',
            'captcha-id':'',
            'login':u'登录'
            }

    u'重写start_requests方法'
    def start_requests(self):
        cookie_jar=CookieJar()
        yield Request(self.start_urls[0],meta={'cookiejar':cookie_jar},callback=self.post_login)

    u'登录方法'
    def post_login(self,response):
        self.log("Preparing to start")
        result=Selector(response)
        self.testCode(result)
        cookie_jar = response.meta['cookiejar']
        cookie_jar.extract_cookies(response, response.request)
        self.saveCookie(self.cookie_file,cookie_jar)
        return [FormRequest.from_response(response,
                            meta={'cookiejar':response.meta['cookiejar']},
                            headers = self.headers,
                            formdata = self.post_data,
                            callback = self.after_login,
                            dont_filter = True
                            )]
    u'登录成功后开始抓取'
    def after_login(self,response):
        cookie_jar = response.meta['cookiejar']
        yield Request(self.start_urls[1],meta={'cookiejar':cookie_jar},callback=self.parse_page)

    u'测试登录是否成功  抓取内容待续。。。'
    def parse_page(self,response):
        result=Selector(response)
        self.log(result.xpath('//title/text()').extract()[0])


    u'以下均为辅助函数  考虑使用协程进行调用'
    def getSrc(self,html):
                content=html.xpath('//div[@class="article"]/form/div[@class="item item-captcha"]/div/img/@src').extract()
                return content

    def getId(self,content):
                return content[0].split('=')[1].split('&')[0]

    u'抓取并保存验证码图片'
    def getImg(self,content):
                img_url=content[0]
                request=urllib2.Request(img_url,headers=self.headers)
                response=urllib2.urlopen(request).read()
                img=open('test.jpg','wb+')
                img.write(response)
                img.close()

    u'检测是否需要验证'
    def testCode(self,result):
        if self.getSrc(result):
            result_src=self.getSrc(result)
            result_id=self.getId(result_src)
            self.getImg(result_src)
            self.post_data['captcha-id']=result_id
            self.post_data['captcha-solution']=raw_input(u'验证码：')
        self.log(self.post_data)

    u'保存cookie'
    def saveCookie(self,file,cookie_jar):
        with open(file, 'wb+') as f:
            for cookie in cookie_jar:
                self.log(cookie)
                f.write(str(cookie) + '\n')