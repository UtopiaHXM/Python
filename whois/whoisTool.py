#!/usr/bin/env python  
# -*- coding: utf-8 -*- 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from tld import get_tld
import urllib
import urllib2
import proxyIP
import re
import phantomjsTools
from scrapy.selector import Selector
import MySQLdb

def getDomainName(href):
	try:
		domainName = get_tld(href)
		return domainName
	except Exception,e:
		print e
		print href
		return None
def getURLResponse(domainName):
	url = 'http://whois.chinaz.com/'+domainName
	print url
	user_agent = proxyIP.user_agent
	headers = {'user_agent':user_agent}
	try:
		req = urllib2.Request(url,headers=headers)
		response = urllib2.urlopen(req)
		body = response.read()
		return body.decode('utf-8')
	except urllib2.HTTPError,e:
		print('HTTPError--code:'+str(e.code))
	except urllib2.URLError,e:
		print('URLError--reason:'+str(e.reason))
def getDetailOnTime(body):
	selector = Selector(text = body,type = 'html')
	info_tag = selector.xpath('//div[contains(@id,"detail")]/div[contains(@class,"div_whois")]/text()').extract()
	if info_tag:
		info = info_tag[0]
		print info
		if info==u'请求数据超时，请与管理员联系。':
			print info
			return False
	else:
		return True

def isPhantomJS(body):
	selector = Selector(text = body,type = 'html')
	img = selector.xpath('string(//div[contains(@id,"loading")]/div[contains(@class,"div_whois")])')
	if img:
		info = img.extract()[0].strip()
		print info
		if info == u'正在努力加载更多信息。。':
			return True
	else:
		print body
		return False
def crawl(url):
	domainName = getDomainName(url)
	if not domainName:
		domainName = url
	body = getURLResponse(domainName)
	isDynamic = isPhantomJS(body)
	print 'isDynamic',isDynamic
	if isDynamic:
		# 判断是否及时加载
		isOnTime = getDetailOnTime(body)
		if isOnTime:
			# 及时加载
			# 域名详细信息由JS异步加载
			# 执行phantomjs加载
			html_str = phantomjsTools.getDom(domainName)
			registry_dict = phantomjsTools.getRegistry(html_str)
			print 'phantomjsTools'
			if registry_dict:
				# 输出返回的注册信息
				print '======================================================='
				for key in registry_dict.keys():
					print key+':'+registry_dict[key]
				print '======================================================='
			return registry_dict
		# 未及时加载
		else:
			print u'未及时加载更多详细信息,请重新查询'
			return None

	else:
		print u'不包含动态加载'
		# 网页注册信息没有js动态加载
		# 直接爬取返回页面的body源码
		# 未知域名
		# 未注册域名
		selector = Selector(text = body,type = 'html')
		info_tag = selector.xpath('//div[contains(@class,"div_whois")]/text()').extract()
		if info_tag:
			info = info_tag[0].strip()
			if info == u'该域名未被注册':
				print info
			elif info==u'未知域名':
				print info
			else:
				print info
		else:
			print u'无正常返回页面,domainName==%s'%domainName
		return None
if __name__ == '__main__':
	url = 'baidu.com'
	crawl(url)
	