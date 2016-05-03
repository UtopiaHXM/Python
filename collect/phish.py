# -*- coding: utf-8 -*-
'''
download csv file from phishtank
http://data.phishtank.com
'''
import urllib
import urllib2
import os
import csv
import MySQLdb
import MySQLdb.cursors
from datetime import datetime
def downloadCVS():
	url = 'http://data.phishtank.com/data/0f41e73f8b9c620658eaebbcca5c09e33c3ad176c633dd59b7004b7f273e2f69/online-valid.csv'
	print 'start downloading with urllib'
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5;Windows NT)'
	headers = {'User-Agent' : user_agent}
	req = urllib2.Request(url,headers = headers)
	try:
		print 'trying'
		response = urllib2.urlopen(req)
		print response
		data = response.read()
		with open('online-valid.csv','wb') as code:
			print 'writing...'
			code.write(data)
	except urllib2.HTTPError, error:
		print 'HTTPError--code:'+str(error.code)
	except urllib2.URLError,error:
		print 'URLError--reason:'+str(error.reason)
	file = open('online-valid.csv','r')
	if file:
		print 'download finished'
		file.close()
		return file
def isExit(filename='online-valid.csv'):
	if os.path.exists(filename):
		try:
			os.remove(filename)
			print 'delete succeed'
		except Exception,e:
			print e
	return os.path.exists(filename)
def formatDateTime(str_datetime):
	date = str_datetime.split('T')[0]
	time = str_datetime.split('T')[-1].split('+')[0]
	datetime_obj = datetime.strptime(date+' '+time,"%Y-%m-%d %H:%M:%S")
	return datetime_obj
def formatData(data):
	for i in range(len(data)):
		data[i] = data[i].replace("'","''")
		data[i] = data[i].replace("\\","\\\\")
	return data
class myDB():
	def __init__(self,host='localhost',user='root',password='root',db='mydb'):
		print 'in __init__'
		self.conn = MySQLdb.connect(host,user,password,db)
		self.cursor = self.conn.cursor()
	def insert(self,column,data):
		sql = "insert into t_phish(%s,%s,%s,%s,%s,%s,%s,%s) values('%s','%s','%s','%s','%s','%s','%s','%s')"%tuple(column+data)
		self.cursor.execute(sql)
		self.conn.commit()
	def selectIsExit(self,data):
		sql = 'select phish_id from t_phish where url="%s"'%(data[1])
		self.cursor.execute(sql)
		result = self.cursor.fetchall()
		if result:
			return True
		else:
			return False
	def __def__(self,):
		print 'in __def__'
		self.cursor.close()
		self.conn.close()
if __name__=='__main__':
	if not isExit():
		downloadCVS()
	if os.path.exists('online-valid.csv'):
		mydbTool = myDB()
		file = open('online-valid.csv','rb')
		column = file.readline().split(',')
		reader = csv.reader(file)
		mydbTool.selectIsExit(column)
		# line = [2910206,http://emmaontheloose.com/4informat32/84yu67.php,
		# http://www.phishtank.com/phish_detail.php?phish_id=2910206,2015-01-14T07:36:17+00:00,
		# yes,2015-01-14T08:05:14+00:00,yes,Other]
		for line in reader:
			line = formatData(line)
			line[3] = formatDateTime(line[3])
			line[5] = formatDateTime(line[5])
			try:
				if not mydbTool.selectIsExit(line):
					mydbTool.insert(column,line)
					print 'info insert succeed'
				else:
					print 'info already exits'
			except Exception,e:
				print e
				print line
		print 'insert finished'