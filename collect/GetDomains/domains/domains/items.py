# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field
class UrlCollections(Item):
	#<p><img src="images/icons/disk.png" alt="download" width="12" height="12" border="0" /> <a href="blocklist.php?download=squiddomain" title="download abuse.ch ZeuS domain blocklist for Squid" target="_parent">download ZeuS domain blocklist for Squid</a></p>
	url = Field()
	title = Field()
	description = Field()
	info_type = Field()
	bad_content = Field()
class DomainsItem(Item):
	info_type = Field()
	bad_content = Field()
	description = Field()

