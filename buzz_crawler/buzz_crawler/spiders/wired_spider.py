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

from w3lib.html import remove_tags_with_content

class WiredSpider(CrawlSpider):
    name = 'wired'
    allowed_domains = ['www.wired.com']
    start_urls = ['http://www.wired.com/']

    def handle_blog(self, response):
        hxs = HtmlXPathSelector(response)
        item = BuzzCrawlerItem()

        item['url'] = response.url
        item['date'] = dateutil.parser.parse(hxs.xpath(".//li[@class='entryDate']/time/@datetime").extract()[0])
        item['title'] = hxs.xpath(".//h1[@id='headline']/text()").extract()[0].strip()
        item['blurb'] = ""

        unprocessed_content = hxs.xpath(".//span[@itemprop='articleBody']").extract()[0]

        sane_html = remove_tags_with_content(unprocessed_content,("noscript","div","h6"))

        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True

        processed_content = h.handle(sane_html)

        if "noscript" in unprocessed_content:
            print sane_html.encode("iso-8859-15", "replace")
            print "*"*98

        item['content'] = markdown(processed_content)
        item['source'] = 'wired.com'
        yield item

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        posts = hxs.xpath(".//div[starts-with(@class,'headline')]/h2")
        
        for post in posts:
            post_link = post.xpath("a/@href").extract()[0]
            post_absolute_url = urlparse.urljoin(response.url, post_link.strip())
            yield Request(post_absolute_url, self.handle_blog)
