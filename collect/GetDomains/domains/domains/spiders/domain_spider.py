# -*- coding: utf-8 -*-
import os
import sys,getopt
path = os.getcwd()[0:-8]
sys.path.append(path)
from scrapy.spider import Spider
from scrapy.selector import Selector
from domains.items import UrlCollections,DomainsItem
from scrapy.http import Request
class DomainSpride(Spider):
    name  = 'domainSpider'
    start_urls = ['https://zeustracker.abuse.ch/blocklist.php']
    #递归爬取
    def reparse(self,response):
            meta = response.meta
            items = []
            contentSelector = Selector(text=response.body,type='html')
            content = contentSelector.xpath('//text()').re(r'([^#|\n]\w.+\S[^#])\n')
            for i in range(len(content)):
                item = DomainsItem()
                item['info_type'] = meta['item']['info_type']
                item['description'] = meta['item']['description']
                item['bad_content'] = content[i]
                items.append(item)
            return items
    def parse(self,response):
        collectHs = response.xpath('//h2[(contains(text(),"domain") and contains(text(),"ZeuS") and not(contains(text(),"Windows"))) or contains(text(),"compromised")]')
        items = []
        for h in collectHs:
            item = UrlCollections()
            item['info_type'] = h.xpath('text()').extract()[0]
            item['description'] = h.xpath('string(following-sibling::p[1])').extract()[0]
            a = h.xpath('following-sibling::p[2]/a[contains(@href,"download")]')
            url = a.xpath('@href').extract()[0]
            if url.startswith('http'):
                item['url'] = url
            else:
                item['url'] = 'https://zeustracker.abuse.ch/'+ url
            item['title'] = a.xpath('@title').extract()[0]
            items.append(item)
        for item in items:
            if item['url']:
                yield Request(url=item['url'],meta={'item':item},callback=self.reparse)
            # if collections:
            #     items = []
            #     for collection in collections:
            #         url = str(collection.xpath('@href').extract()[0])
            #         if url.startswith('http'):
            #             item['url'] = collection.xpath('@href').extract()[0]
            #         else:
            #             item['url'] = 'https://zeustracker.abuse.ch/'+ str(collection.xpath('@href').extract()[0])
            #         item['title'] = collection.xpath('@title').extract()
            #         item['describe'] = collection.xpath('text()').extract()
            #         items.append(item)
            #     for item in items:
            #         if item['url']:
                        #yield Request(url=item['url'],meta={'item':item},callback=self.reparse)
