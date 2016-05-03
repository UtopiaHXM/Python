# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from items import UrlCollections
from scrapy import log
from twisted.enterprise import adbapi
import MySQLdb.cursors
import MySQLdb
class DomainsPipeline(object):
	def __init__(self):
		self.dbpool = adbapi.ConnectionPool('MySQLdb',db='mydb',user='root',passwd='root',
			cursorclass=MySQLdb.cursors.DictCursor,
			charset='utf8',use_unicode=True)
		log.msg('log in init',level = log.INFO)
	
	def handler_err(self,e):
		log.err(e)

	def insert_item(self,tx,item):
		#url,title,info_type,bad_content,description
		tx.execute("select * from t_zeustracker where bad_content=%s",(item['bad_content'],))
		result = tx.fetchall()
		print result
		if result:
			log.msg("Insert failed::this domain %s has exited"%item['bad_content'],level=log.DEBUG)
		else:
			tx.execute("insert into t_zeustracker(info_type,bad_content,description) values (%s,%s,%s)",(item['info_type'],item['bad_content'],item['description']))
			log.msg("Insert success::this domain %s has inserted"%item['bad_content'],level=log.DEBUG)

	def process_item(self, item, spider):
		query = self.dbpool.runInteraction(self.insert_item,item)
		query.addErrback(self.handler_err)
		return item
