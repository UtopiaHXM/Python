#!/usr/bin/env python  
# -*- coding: utf-8 -*- 
import urllib2
import urllib
import requests
import MySQLdb
import simplejson
from datetime import datetime
import time
from simplejson.scanner import JSONDecodeError
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
	# def isExitScan_id(self,scan_id):
	# 	sql = 'select scan_id from t_virusapi where scan_id="%s"'%scan_id
	# 	self.cursor.execute(sql)
	# 	result = self.cursor.fetchall()
	# 	if result:
	# 		return True
	# 	else:
	# 		return False
	def isExitURL(self,url):
		sql = 'select scan_id from t_virusapi where url="%s"'%url
		try:
			self.cursor.execute(sql)
			result = self.cursor.fetchall()
			if result:
				return True
			else:
				return False
		except Exception,e:
			print e
			print url
			return False
	def insert(self,item):
		# 获取url-report返回数据的keys,对basestring类型的格式化字符串
		try:
			for key in item.keys():
				if item.has_key(key) and key in ['response_code','scan_id','url','scan_date','positives','total','scans']:
					value = item.get(key)
					if isinstance(value,dict):
						#print 'value:','scans_dict'
						for sub_key in value.keys():
							if value.get(sub_key).get('detected')==False:
								value.pop(sub_key)
						item[key] = str(value).replace("'","''").replace('\\','\\\\')
					if isinstance(value,basestring):
						#print 'item[%s]'%key,item[key]
						item[key] = value.replace("'","''").replace('\\','\\\\')
				else:
					item.pop(key)
			column = tuple(item.keys())
			values = tuple(item.values())
			insert_column = ''
			insert_values = ''
			for index,col in enumerate(column):
				insert_column += col
				if index!=len(column)-1:
					insert_column += ','
			for index,value in enumerate(values):
				insert_values += "'"+str(value)+"'"
				if index!=len(values)-1:
					insert_values += ','
			#print insert_column,insert_values
			sql = 'insert into t_virusapi(%s) values (%s)'%(insert_column,insert_values)
			#print sql
			self.cursor.execute(sql)
			self.conn.commit()
			return True
		except Exception,e:
			print e
			return False
def divList(sub_length,result_list):
	length = len(result_list)
	groups = length/sub_length
	#print 'groups',groups
	result = []
	temp = []
	#print 'result_list',length
	for i in range(length):
		if i<(groups*sub_length):
			temp.append(result_list[i])
			if len(temp)==sub_length:
				result.append(temp)
				temp = []
		else:
			temp.append(result_list[i])
			if i==length-1:
				result.append(temp)
	return result
def reportURL(urls,apikey):
	#print urls
	url = "https://www.virustotal.com/vtapi/v2/url/report"
	parameters = {"resource": urls, "apikey": apikey,"scan":1,"allinfo":1}
	try:
		response = requests.post(url, parameters)
		json = response.json()
		return json
	except urllib2.HTTPError, error:
		print 'HTTPError--code:'+str(error.code)
		return None
	except urllib2.URLError,error:
		print 'URLError--reason:'+str(error.reason)
		return None
	except Exception,e:
		print e
		return None
if __name__ == '__main__':
	apikey = 'e3c12bf4eea6b61e25a45601d0d848dc36a8ede5499688129920c6e4240ad20d'
	db = mydb()
	malware = db.getMalUrls()
	phish = db.getPhishUrls()
	zeus = db.getZeusUrls()
	group_list = malware + phish + zeus
	for url in group_list:
		if db.isExitURL(url[0].replace('\\','\\\\').replace("'","''")):
			print 'url_info has already exits detect url'
		else:
			detect_url = url[0].replace("''","'").replace('\\\\','\\')
			#开始获取不存在的url-report,当url不存在时默认提交分析报告，scan=1
			report_json = reportURL(detect_url,apikey)
			#print 'report_json',report_json
			if not report_json:
				times = 0
				while times<3 and not report_json:
					report_json = reportURL(detect_url,apikey)
					times += 1
					print 'analysis %s times'%str(times)
				if not report_json:
					print 'analysis 3 times failed'
					continue
			report_json['url'] = detect_url

			if report_json:
				# for key in report_json.keys():
				# 	print key,report_json.get(key)
				if db.insert(report_json):
					print 'insert succeed'
