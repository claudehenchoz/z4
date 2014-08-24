from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider  # Rule
from scrapy.http.request import Request
import html2text
import time
import re
import dateutil.parser
import datetime
import urlparse
from buzz_crawler.items import BuzzCrawlerItem
from markdown import markdown


class WozSpider(CrawlSpider):
    name = 'woz'
    allowed_domains = ['www.woz.ch']
    start_urls = ['http://www.woz.ch/']

    def handle_blog(self, response):
        hxs = HtmlXPathSelector(response)
        item = BuzzCrawlerItem()

        item['url'] = response.url

        item['date'] = datetime.datetime.now()
        item['title'] = hxs.xpath(".//*[@id='container']/div/div/article/header/h1/text()").extract()[0].strip()
        item['blurb'] = hxs.xpath(".//*[@id='container']/div/div/article/header/h2/text()").extract()[0].strip()

        unprocessed_content = hxs.xpath("//div[@class='article-content']").extract()[0].strip()
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        processed_content = h.handle(unprocessed_content)

        item['content'] = markdown(processed_content)
        item['source'] = 'woz.ch'
        yield item

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        posts = hxs.xpath(".//*[@id='container']/div/div/article")
        
        for post in posts:
            post_link = post.xpath("a/@href").extract()[0]
            post_absolute_url = urlparse.urljoin(response.url, post_link.strip())
            yield Request(post_absolute_url, self.handle_blog)
