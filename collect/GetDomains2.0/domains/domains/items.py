# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field
class DomainsItem(Item):
    # define the fields for your item here like:
    Date_update = Field()
    Domain = Field()
    IP = Field()
    Reverse_Lookup = Field()
    Description = Field()
    Registrant = Field()
    ASN = Field()
    Country = Field()
