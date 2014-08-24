# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from django.db.utils import IntegrityError

class BuzzCrawlerPipeline(object):
    def process_item(self, item, spider):
        try:
            item.save()
        except IntegrityError:
            print(">>> Item exists already, dropping")

        return item
