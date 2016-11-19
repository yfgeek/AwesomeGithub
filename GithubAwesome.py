#-*- coding: utf-8 -*-
# Code by Ivan
# Automatically get some awesome project or repo from your following user everyday
#
# The first line of comments is English version
#
# Welcome to pull request
# Enjoy!
# Site:github.com/yfgeek

import os
import re
import sys
import urllib
import urllib2
import time
import cookielib
from bs4 import BeautifulSoup

class GithubAwesome(object):

    # Initializaiton Constructor
    def __init__(self,name,password):
        self.user = name
        self.password = password
        self.cookie = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        urllib2.install_opener(self.opener)
        getCookieUrl = "https://github.com/login"
        self.html = urllib2.urlopen(getCookieUrl).read()

    # Browse the page to get Cookie
    def _get_headers(self,referer):
        headers = {}
        headers['User-Agent']='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        headers['Connection']='keep-alive'
        headers['Cache-Control']='max-age=0'
        headers['Accept-Language']='zh-CN,zh;q=0.8,en;q=0.6'
        headers['Accept']='text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        headers['Referer']= referer
        return headers

    # sign in github.com
    def login(self):
        print "Getting the authenticity_token"
        token = self.__get_user_token(self.html)[0]
        loginparams = {
        'commit' : 'Sign in',
        'utf8' : '%E2%9C%93',
        'authenticity_token' : token,
        'login' : self.user,
        'password' : self.password
        }
        # post loginparams to login
        req = urllib2.Request( 'https://github.com/session', urllib.urlencode(loginparams), headers=self._get_headers('https://github.com/login'))
        tmp = 0
        try:
            resp = urllib2.urlopen(req)
        except :
            if (tmp <100):
                print 'Network conditions is not good.Reloading.'
                self.login(self)
            else:
                print 'Fail to get it' + img['src']
                pass
                tmp = tmp +1

        self.operate = self.opener.open(req)
        thePage = resp.read().decode("utf-8")
        # print the result of login
        print token
        print "Login Successful \n"
        return thePage

    # Get the userToken
    def __get_user_token(self,part):
        reg = re.compile('authenticity_token".*?value="(.*?)".*?>');
        result = re.findall(reg,part)
        return result

    # get the repo html sourcecode and return each part of staring or forking information from your following friend
    def __get_repo(self,part):
        soup = BeautifulSoup(part,"html.parser")
        result = soup.find_all("div",{"class":"body"})
        return result

    # get the url of each repo
    def __get_url(self,part):
        part = str(part)
        rs = BeautifulSoup(part,"html.parser")
        result = "http://github.com" + str(rs.find_all('a')[1]["href"])
        return result

    # get the status of star, fork, decription from the url input in
    def get_status(self,url):
        req = urllib2.Request(url,headers=self._get_headers(''))
        try:
            response = urllib2.urlopen(req)
        except Exception, e:
            print "Retrying..."
        else:
            pass
        self.opener.open(req)
        thePage = response.read()
        soup = BeautifulSoup(thePage,"html.parser")
        try:
            description = str(soup.find("span",attrs={"itemprop":"about"}).string).replace('\n','')
        except Exception, e:
            description = ' None'

        result = soup.find_all("a",{"class":"social-count"})
        dict = {'star':0,'fork':0}
        try:
            dict['star'] = int(result[2].string.replace('\n','').replace('\t','').replace(' ','').replace(',',''))
            dict['fork'] = int(result[3].string.replace('\n','').replace('\t','').replace(' ','').replace(',',''))
            dict['description'] = description
        except Exception, e:
            dict['star'] = 0
            dict['fork'] = 0
        return dict

    # get awesome from pages
    def get_awesome(self,page,minstar,minfork):
        url = "https://github.com/dashboard/index/" + str(page)
        req = urllib2.Request(url,headers=self._get_headers(''))
        try:
            response = urllib2.urlopen(req)
        except Exception, e:
            print "Retrying..."
        else:
            pass
        self.opener.open(req)
        thePage = response.read()
        repo = self.__get_repo(thePage)
        startmp = 0
        forktmp = 0
        for re in repo:
            url = self.__get_url(re)
            status = self.get_status(url)
            star =  status.get('star')
            fork =  status.get('fork')
            if star>minstar or fork>minfork:
                if (startmp != star) & (forktmp != fork):
                    print '🔥  ' + url
                    print '⭐️  Star: ' + str(status.get('star')) + ' 🍴  Fork :' + str(status.get('fork'))
                    print  status.get('description') + '\n'
                startmp =  star
                forktmp =  fork


if __name__ == '__main__':
    default_encoding = 'utf-8'
    if sys.getdefaultencoding() != default_encoding:
        reload(sys)
        sys.setdefaultencoding(default_encoding)
        # new object GithubFollow with parm1:username parm2:password
        ga = GithubAwesome('username','password')
        # login
        ga.login()
        # get awesome repo param is the page you want to see
        ga.get_awesome(1,50,50) # page 1
        # TODO try to output the result into markdown file or html file
        # TODO try to watch every pages and output the result automatically
