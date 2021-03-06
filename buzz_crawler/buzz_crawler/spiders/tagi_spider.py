from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider  # Rule
from scrapy.http.request import Request
import html2text
import time
import re
import datetime
import dateutil.parser
import urlparse
from buzz_crawler.items import BuzzCrawlerItem
from markdown import markdown


class TagiSpider(CrawlSpider):
    name = 'tagi'
    allowed_domains = ['www.tagesanzeiger.ch']
    start_urls = ['http://www.tagesanzeiger.ch/']

    def handle_blog(self, response):
        hxs = HtmlXPathSelector(response)
        item = BuzzCrawlerItem()

        item['url'] = response.url
        item['title'] = hxs.xpath("//div[@id='article']/h1/text()").extract()[0].strip()
        item['blurb'] = hxs.xpath("//div[@id='article']/h3/text()").extract()[0].strip()

        unprocessed_content = hxs.xpath("//div[@id='mainContent']").extract()[0]

        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True

        processed_content = h.handle(unprocessed_content)

        item['content'] = markdown(processed_content)
        item['source'] = 'tagesanzeiger.ch'
        yield item

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        posts = hxs.xpath("//div[@class='featureStory standard']")
        
        for post in posts:
            post_link = post.xpath("h3/a/@href").extract()[0]
            post_absolute_url = urlparse.urljoin(response.url, post_link.strip())
            yield Request(post_absolute_url, self.handle_blog)
