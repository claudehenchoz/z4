# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

#from scrapy.item import Item, Field

from scrapy.contrib.djangoitem import DjangoItem
from buzz.models import BuzzItem

class BuzzCrawlerItem(DjangoItem):
    django_model = BuzzItem
