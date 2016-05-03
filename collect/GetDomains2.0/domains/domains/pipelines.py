# -*- coding: utf-8 -*-

# Define your item pipelines here
# 
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from items import DomainsItem
from scrapy import log
from twisted.enterprise import adbapi
import MySQLdb.cursors
import MySQLdb
class DomainsPipeline(object):
	def __init__(self):
		self.dbpool = adbapi.ConnectionPool('MySQLdb',db='mydb',user='root',passwd='root',
			cursorclass=MySQLdb.cursors.DictCursor,
			charset='utf8',use_unicode=True)
		log.msg('log in init ',level = log.INFO)

	def handler_err(self,e):
		log.err(e)

	def insert_item(self, tx, item):
		tx.execute("select * from t_malware where Date_update = %s and Domain = %s and IP = %s and Reverse_Lookup = %s and Description = %s and Registrant = %s\
			and ASN = %s and Country = %s",(item['Date_update'],item['Domain'],item['IP'],item['Reverse_Lookup'],item['Description'],item['Registrant'],item['ASN'],item['Country']))
		result = tx.fetchall()
		if result:
			log.msg("Insert failed::Domain %s has exited::" % item['Domain'],level = log.DEBUG)
		else:
			tx.execute("insert into t_malware (Date_update,Domain,IP,Reverse_Lookup,Description,Registrant,\
				ASN,Country) values (%s,%s,%s,%s,%s,%s,%s,%s)",(item['Date_update'],item['Domain'],
				item['IP'],item['Reverse_Lookup'],item['Description'],item['Registrant'],
				item['ASN'],item['Country'])
			)
			print 'Insert over'
			log.msg("Insert success::Domain has inserted ",level = log.DEBUG)

	def process_item(self, item, spider):
		query = self.dbpool.runInteraction(self.insert_item,item)
		query.addErrback(self.handler_err)
		return item
