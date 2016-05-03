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
#禁止cookies
COOKIES_ENABLED = False

DOWNLOAD_DELAY = 0

DOWNLOADER_MIDDLEVARES = {
	'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
	'domains.middlewares.ProxyMiddleware':100,
	'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware':None,
	'domains.middlewares.UserAgentMiddleware':543
}

ITEM_PIPELINES = ['domains.pipelines.DomainsPipeline']

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'domains (+http://www.yourdomain.com)'
