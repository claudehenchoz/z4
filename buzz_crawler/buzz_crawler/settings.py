# Scrapy settings for buzz_crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

import sys
sys.path.append('C:\\Users\\Claude\\Documents\\z4')

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'z4.settings'


BOT_NAME = 'buzz_crawler'

SPIDER_MODULES = ['buzz_crawler.spiders']
NEWSPIDER_MODULE = 'buzz_crawler.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'buzz_crawler (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
    'buzz_crawler.pipelines.BuzzCrawlerPipeline': 1000,
}
