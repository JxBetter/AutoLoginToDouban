# -*- coding: utf-8 -*-
import scrapy
import urllib.request
from scrapy.http import Request,FormRequest


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    '''start_urls = ['http://douban.com/']'''
    head = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.2372.400 QQBrowser/9.5.10771.400'}
    def start_requests(self):
        yield Request(url='https://accounts.douban.com/login',callback=self.parse,headers=self.head,meta={'cookiejar':1})


    def parse(self, response):
        post_url = 'https://accounts.douban.com/login'
        yzm = response.xpath('//img[@id="captcha_image"]/@src').extract()
        post_data = {'form_email':'XXXXXXXX',
                     'form_password':'XXXXXXX',
                     'redir':'XXXXXXXX'#登陆成功后跳转到的网址
                     }
        if len(yzm) == 0:
            print('无验证码')
            return [FormRequest.from_response(response,
                                            meta={'cookiejar':response.meta['cookiejar']},
                                            headers=self.head,
                                            formdata=post_data,
                                            callback=self.backfun,)]
        else:
            print('有验证码')
            imgpath = 'E:/python/20171103/yzm.jpg'
            urllib.request.urlretrieve(yzm[0],filename=imgpath)
            yzmval = input('请输入验证码')
            post_data['captcha-solution'] = yzmval
            return [FormRequest.from_response(response,
                                      meta={'cookiejar': response.meta['cookiejar']},
                                      formdata=post_data,
                                      headers=self.head,
                                      callback=self.backfun,)]

    def backfun(self,response):
        user = response.xpath('//head/title/text()').extract()
        print('登陆成功')
        print(user[0])
