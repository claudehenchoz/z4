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


class LizSpider(CrawlSpider):
    name = 'liz'
    allowed_domains = ['www.limmattalerzeitung.ch']
    start_urls = ['http://www.limmattalerzeitung.ch/']

    def handle_blog(self, response):
        hxs = HtmlXPathSelector(response)
        item = BuzzCrawlerItem()

        item['url'] = response.url
        item['title'] = hxs.xpath(".//*[@id='articledetail']/div/h1/text()").extract()[0].strip()
        item['blurb'] = hxs.xpath(".//*[@id='articledetail']/div/div[@class='box anriss']/text()").extract()[0].strip()

        unprocessed_content = hxs.xpath(".//*[@id='articletextcontent-narrow']/div[@class='article-text billableContent']").extract()[0].strip()
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        processed_content = h.handle(unprocessed_content)

        item['content'] = markdown(processed_content)
        item['source'] = 'limmattalerzeitung.ch'
        yield item

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        posts = hxs.xpath(".//a[@class='heading']")
        
        for post in posts:
            post_link = post.xpath("@href").extract()[0]
            post_absolute_url = urlparse.urljoin(response.url, post_link.strip())
            yield Request(post_absolute_url, self.handle_blog)
