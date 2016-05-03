#!/usr/bin/env python  
# -*- coding: utf-8 -*- 
import urllib2
import MySQLdb
import time
class mydb:
	def __init__(self,host='localhost',user='root',password='root',db='mydb'):
		print 'in __init__'
		self.conn = MySQLdb.connect(host,user,password,db)
		self.cursor = self.conn.cursor()
	def getMalUrls(self):
		sql = 'select Domain from t_malware where Domain != "-" '
		self.cursor.execute(sql)
		result = self.cursor.fetchall()
		#print 'Malware:',result
		return result
	def getPhishUrls(self):
		sql = 'select url from t_phish'
		self.cursor.execute(sql)
		result = self.cursor.fetchall()
		#print 'Phish:',result
		return result
	def getZeusUrls(self):
		sql = 'select bad_content from t_zeustracker'
		self.cursor.execute(sql)
		result = self.cursor.fetchall()
		#print info_type,result
		return result
	def isExit(self,url):
		#url_type = data.get('type')
		#sql = 'select id,url,type from t_safebrowsing where url="%s" and type="%s"'%(url,url_type)
		sql = 'select id,url,type from t_safebrowsing where url="%s"'%url
		print sql
		self.cursor.execute(sql)
		result = self.cursor.fetchall()
		if result:
			return True
		else:
			return False
	def insert(self,result):
		if result:
			column = ('url','type') 
			data = (result.get('url'),result.get('type'))
			try:
				sql = "insert into t_safebrowsing(%s,%s) values('%s','%s')"%tuple(column+data)
				#print sql
				self.cursor.execute(sql)
				self.conn.commit()
				print 'succeed',sql
			except Exception, e:
				print 'Exception::',e
				print 'failed',sql
				return False
			print 'insert success'
			return True
		else:
			return False
	def __def__(self):
		print 'in __def__'
		self.cursor.close()
		self.conn.close()
def formateData(url):
	if url:
		if isinstance(url,basestring):
			return url.replace("'","''").replace("\\","\\\\")
	else:
		return None	
def divList(result_list):
	print len(result_list)
	if len(result_list)<10000:
		return result_list
	else:
		length = len(result_list)
		groups = length/10000
		result = []
		temp = []
		#print 'result_list',length
		for i in range(length):
			if i<(groups*10000):
				temp.append(result_list[i])
				if len(temp)==10000:
					result.append(temp)
					temp = []
			else:
				temp.append(result_list[i])
				if i==length-1:
					result.append(temp)
		return result
def fomateURL(url):
	detect_url = '1\n'+url+'\n'
	return detect_url
	# return detect_url.replace("'","''").replace('\\','\\\\')
def detectURL(client,apikey,appver,pver,detect_url):
	response = ''
	toURL = 'https://sb-ssl.google.com/safebrowsing/api/lookup?client=%s&key=%s&appver=%s&pver=%s'%(client,apikey,appver,pver)
	try:
		response = urllib2.urlopen(toURL, detect_url)
	except urllib2.HTTPError,error:
		print 'HTTPError--code:'+str(error.code)
	except urllib2.URLError,error:
		print 'URLError--reason:'+str(error.reason)
	except Exception, e:
		if hasattr(e, 'code') and e.code == httplib.NO_CONTENT: # 204
			print toURL, detect_url 
			print "No match"
		elif hasattr(e, 'code') and e.code == httplib.BAD_REQUEST: # 400
			print "Invalid request"
		elif hasattr(e, 'code') and e.code == httplib.UNAUTHORIZED: # 401
			print "Invalid API key"
		elif hasattr(e, 'code') and e.code == httplib.FORBIDDEN: # 403 (should be 401)
			print "Invalid API key"
		elif hasattr(e, 'code') and e.code == httplib.SERVICE_UNAVAILABLE: # 503
			print "Server error, client may have sent too many requests"
		else:
			print "Unexpected server response"
	else:
		url_type = response.read()
		if not url_type:
			print "No match"
			url_type = 'no_content'
		else:
			print "At least 1 match"
		print url_type
		return url_type
if __name__ == '__main__':
	client ='SafeBrowsingUrl'
	apikeys = ['AIzaSyC-pt1qTG6sdvnzKAbe3uf7L-6wwil2NqY',
	'AIzaSyCCXXMNp8dtcX-rrKUCxPf0d0g4Se1ym2w',
	'AIzaSyADx635BlXecDbu6ojUtStQLwXgLWpxcg4',
	'AIzaSyCgs7_TLUC6TAw-WZYE1VXmZEF1WYQ4W9Q',
	'AIzaSyAmzDKdgHNmuobbVXNAH2LHKYJULpeErKI',
	'AIzaSyAExAOti6ooSiP1o6TsPolOMHWA9uwEpW8',
	'AIzaSyBc8MdkFgoDENskiFR-ZWyJKs-vLhCPXSg',
	'AIzaSyDV2eBkspbEguJ5TRg2H2r1x2s-Peb9xhs',
	'AIzaSyDQkKb8vaQ3m7lopyXGxnaM9kTK8VfpEqw',
	'AIzaSyCiaZF7Ao5d9G6vz8Rdb3RwVh1XptLnK78',
]
	appver = '1.0'
	pver = '3.1'
	db = mydb()
	malware = db.getMalUrls()
	phish = db.getPhishUrls()
	zeus = db.getZeusUrls()
	url_list = divList(malware+phish+zeus)
	#print 'url_list',len(url_list)
	for index,url in enumerate(url_list):
		print index
		for item in url:
			#item::('cdn02.heartbleedporn.com:25707/chart/dict/movies.php?timeline=21',)
			insert_url = formateData(item[0])	#return url
			print insert_url
			if db.isExit(insert_url):
				print 'already exits'
			else:
				detect_url = fomateURL(item[0])
				url_type =  detectURL(client,apikeys[index],appver,pver,detect_url)
				if url_type:
					data = {'url':insert_url,'type':url_type}
					db.insert(data)
				else:
					print 'no_type',insert_url
		#print 'sleep 24h'
		#time.sleep(1*60*60*24)

