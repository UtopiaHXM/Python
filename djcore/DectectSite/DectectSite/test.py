#!/usr/bin/env python
#-*-coding:utf-8-*-
'''
home:http://www.hitwh.edu.cn/
'''
import urllib2
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
def scrapy():
  url = "https://www.virustotal.com"
  user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5;Windows NT)'
  headers = {'User-Agent' : user_agent}
  req = urllib2.Request(url,headers = headers)
  try:
    print 'trying'
    response = urllib2.urlopen(req)
    html = response.read()
    print html
  except urllib2.HTTPError, error:
    print 'HTTPError--code:'+str(error.code)
  except urllib2.URLError,error:
    print 'URLError--reason:'+str(error.reason)
if __name__ == '__main__':
  scrapy()
