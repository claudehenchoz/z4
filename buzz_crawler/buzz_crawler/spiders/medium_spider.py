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


class MediumSpider(CrawlSpider):
    name = 'medium'
    allowed_domains = ['medium.com']
    start_urls = ['https://medium.com/']

    def handle_blog(self, response):
        hxs = HtmlXPathSelector(response)
        item = BuzzCrawlerItem()

        item['url'] = response.url
        item['title'] = hxs.xpath(".//div[@class='section-inner layoutSingleColumn']/h2/text()|.//div[@class='section-inner layoutSingleColumn']/h3/text()").extract()[0].strip()
        item['blurb'] = hxs.xpath(".//div[@class='section-inner layoutSingleColumn']/h4/text()|.//div[@class='section-inner layoutSingleColumn']/p/text()").extract()[0].strip()

        unprocessed_content = hxs.xpath(".//div[@class='section-inner layoutSingleColumn']").extract()[1]
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        processed_content = h.handle(unprocessed_content)

        item['content'] = re.sub('(?s)<h3>Recommended<\/h3>.*<\/ul>', '', markdown(processed_content))
        item['source'] = 'medium.com'
        yield item

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        posts = hxs.xpath(".//h3[@class='block-title']")
        
        for post in posts:
            post_link = post.xpath("a/@href").extract()[0]
            post_absolute_url = urlparse.urljoin(response.url, post_link.strip())
            yield Request(post_absolute_url, self.handle_blog)
