#!/usr/bin/env python  
# -*- coding: utf-8 -*- 
import urllib2
import requests
apikey = 'e3c12bf4eea6b61e25a45601d0d848dc36a8ede5499688129920c6e4240ad20d'
def analysis(json):
	try:
		for key in json.keys():
			if json.has_key(key) and key in ['scan_date','positives','total','scans']:
				value = json.get(key)
				if isinstance(value,dict):
					print 'isinstance'
					info = '\n'
					for sub_key in value.keys():
						if value.get(sub_key).get('detected')==True:
							info += sub_key+':'+value.get(sub_key).get('result')
							info += '\n'
					json[key] = info
			else:
				json.pop(key)
		return json
	except Exception,e:
		print e
		return False
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
	
	report_json = reportURL('www.baidu.com',apikey)
			#print 'report_json',report_json
	if not report_json:
		times = 0
		while times<3 and not report_json:
			report_json = reportURL('www.baidu.com',apikey)
			times += 1
			print 'analysis %s times'%str(times)
		if not report_json:
			print 'analysis 3 times failed'
	if report_json:
		result = analysis(report_json)
		print result.items()
