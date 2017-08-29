# -*- coding:utf-8 -*-
import requests
from HTMLParser import HTMLParser
class DoubanClient(object):
    def __init__(self):
        object.__init__(self)
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
                   }
        self.session = requests.Session()
        self.session.headers.update(headers)
    def login(self, username, pw, source='登陆', redir='https://www.douban.com/people/165763334/',
               login='登陆'):
        url='https://accounts.douban.com/login'
        r=self.session.get(url)
        (id,img_url)=_get_captcha(r.content)
        print 'id-%s'%id
        print 'img_url-%s'%img_url

        if id:
            captcha_solution=raw_input('please input solution for (%s):'%img_url)
        ck = _get_ck(r.content)
        print 'ck-%s'%ck
        data={
              'form_email': username,
              'form_password': pw,
              'source': source,
              'redir':redir,
              'login':login}
        if ck:
            data['ck'] = ck
        if id:
            data['captcha-id'] = id
            data['captcha-solution'] = captcha_solution
        headers={'Referer': 'https://www.douban.com/accounts/login?redir=https%3A//www.douban.com/people/165763334/',
                   'Upgrade-Insecure-Requests': '1',
                   'Host':'accounts.douban.com',
                   'Origin':'https://www.douban.com'}
        self.session.post(url,data=data,headers=headers)
        print(self.session.cookies.items())
    def edit_signature(self, signature):
        url = 'https://www.douban.com/people/165763334/'

 #       ck=_get_ck(r.content)
        ck = self.session.cookies['ck']
        url = 'https://www.douban.com/j/people/165763334/edit_signature'
        headers = {'referer': 'https://www.douban.com/people/165763334/',
                   'host': 'www.douban.com',
                   'x-requested-with': 'XMLHttpRequest'}
        data = {'ck': ck, 'signature': signature}
        print 'ck-%s'%ck
        r=self.session.post(url, data=data, headers=headers)
        print r.content


def _attr(attrs, attrname):
    for attr in attrs:
        if attr[0] == attrname:
            return attr[1]
    return None

def _get_captcha(content):
    class CaptchaParser(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.id=None
            self.img_url=None
        def handle_starttag(self, tag, attrs):
            if tag=='input' and _attr(attrs,'type')=='hidden'\
                and _attr(attrs,'name')=='captcha-id':
                self.id=_attr(attrs,'value')
            if tag=='img' and _attr(attrs,'id')=='captcha_image'\
                and _attr(attrs,'class')=='captcha_image':
                self.img_url=_attr(attrs,'src')
    p = CaptchaParser()
    p.feed(content)
    return p.id, p.img_url

def _get_ck(content):
    class CkParser(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.ck=None
        def handle_starttag(self, tag, attrs):
            if tag=='input' and _attr(attrs,'type')=='hidden'\
                and _attr(attrs,'name')=='ck':
                self.id=_attr(attrs,'value')
    p = CkParser()
    p.feed(content)
    return p.ck
if __name__ == '__main__':
    d = DoubanClient()
    d.login('703048413@qq.com', 'a703048413')
    d.edit_signature('haha')