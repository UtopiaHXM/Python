# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

# Scrapy settings for domains project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'domains'

SPIDER_MODULES = ['domains.spiders']
NEWSPIDER_MODULE = 'domains.spiders'
ITEM_PIPELINES = ['domains.pipelines.DomainsPipeline']
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'domains (+http://www.yourdomain.com)'
