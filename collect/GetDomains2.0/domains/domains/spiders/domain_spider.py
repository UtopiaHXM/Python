# -*- coding: utf-8 -*-
import os
import sys
path = os.getcwd()[0:-8]
sys.path.append(path)
import string
from datetime import datetime
from scrapy.spider import Spider
from scrapy.selector import Selector
from domains.items import DomainsItem
from scrapy.http import Request
class DomainSpride(Spider):
    name  = 'domainSpider'
    start_urls = ['http://www.malwaredomainlist.com/mdl.php']
    #def __init__(self):
        #self.file_log = open('C:/IPs/log.txt','w+') 
    #递归爬取
    def reparse(self,response):
        #file = open('C:/IPs/'+current_page+'.txt','w+')
        if response.status == 200:
            #print 'start'
            #self.file_log.write(response.url+'\n')
            #<table class="table">
            #<tr bgcolor="#d8d8d8" onmouseover="this.style.backgroundColor='#b6bac6'" onmouseout="this.style.backgroundColor='#d8d8d8'">
            #0--<td><nobr>2014/12/18_11:17</nobr></td>
            #1--<td>andreyzakharov.com/w<wbr>p-content/plugins/wp<wbr>-no-category-base/ge<wbr>neric/</td>
            #2--<td>77.222.56.213</td>
            #3--<td>vh87.sweb.ru.</td>
            #4--<td>redirects to AppleId<wbr> phishing</td>
            #5--<td>Registrar Abuse Cont<wbr>act onlinenic-enduse<wbr>r@onlinenic.com</td>
            #6--<td>44112</td>
            #7--<td align="center"><img src="images/blank.gif" class="flags flag-RU" alt="RU" title="Russia"/></td>
            #</tr>
            #</table>
            items = []
            selector = Selector(text = response.body,type = 'html')
            collections = selector.xpath('//table[contains(@class,"table")]')[-1].xpath('//tr[contains(@onmouseover,"this.style.backgroundColor")]')
            key_list = {
                '0':'Date_update',
                '1':'Domain',
                '2':'IP',
                '3':'Reverse_Lookup', 
                '4':'Description',
                '5':'Registrant',
                '6':'ASN',
                '7':'Country'}
            for collection in collections:
                items_len = len(collection.xpath('td'))
                item = DomainsItem()
                for i in range(0,items_len-1):
                    index = 'string(td[%d])'%(i+1)
                    key = key_list[str(i)]
                    if key=='Date_update':
                        value = collection.xpath(index).extract()[0].replace('_',' ')
                        item[key] = datetime.strptime(value,"%Y/%m/%d %H:%M")
                    else:
                        item[key] = collection.xpath(index).extract()[0]
                    #file.write(('item[%s]'%key)+':'+collection.xpath(index).extract()[0]+'\n')
                item['Country'] = collection.xpath('//td/img/@title').extract()[0]
                #file.write('item[Country]:'+item['Country']+'\n')
                items.append(item)
                #file.write('\n')
            return items
    def parse(self,response):
            #爬取网页信息
            #self.file_log.write('response.url=='+str(response.url))
            #<center>
            #<p>Page 
            #<a href="mdl.php?inactive=&amp;sort=Date&amp;search=&amp;colsearch=All&amp;ascordesc=DESC&amp;quantity=100&amp;page=0">0
            #</a> 
            #<a href="mdl.php?inactive=&amp;sort=Date&amp;search=&amp;colsearch=All&amp;ascordesc=DESC&amp;quantity=100&amp;page=1">1</a> 
            #... 
            #<a href="mdl.php?inactive=&amp;sort=Date&amp;search=&amp;colsearch=All&amp;ascordesc=DESC&amp;quantity=100&amp;page=33">33
            #</a>
            #</p>
            #</center>
            pageNum = response.xpath('//center/p/a[contains(@href,"page")]/text()').extract()[-1]
            #需要爬取的网页数量
            print pageNum
            #http://www.malwaredomainlist.com/mdl.php?inactive=&sort=Date&search=&colsearch=All&ascordesc=DESC&quantity=100&page=0
            for i in range(0,string.atoi(pageNum)+1):
                url  = 'http://www.malwaredomainlist.com/mdl.php?inactive=&sort=Date&search=&colsearch=All&ascordesc=DESC&quantity=100&page='
                url = url + str(i)
                yield Request(url,meta={'current_page':i},callback=self.reparse)