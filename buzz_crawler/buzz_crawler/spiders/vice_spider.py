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


class ViceSpider(CrawlSpider):
    name = 'vice'
    allowed_domains = ['www.vice.com']
    start_urls = ['http://www.vice.com/en_us/']

    def handle_blog(self, response):
        hxs = HtmlXPathSelector(response)
        item = BuzzCrawlerItem()

        item['url'] = response.url
        item['date'] = datetime.datetime.now()
        item['title'] = hxs.xpath("//h1[@class='article-title']/text()").extract()[0].strip()
        item['blurb'] = ""

        unprocessed_content = hxs.xpath("//div[@class='article_content']").extract()[0]
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        processed_content = h.handle(unprocessed_content)

        item['content'] = re.sub('(?s)<h3>Recommended<\/h3>.*<\/ul>', '', markdown(processed_content))
        item['source'] = 'vice.com'
        yield item

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        posts = hxs.xpath("//ul[@class='story_list shows_grid_list']/li")
        
        for post in posts:
            post_link = post.xpath("a/@href").extract()[0]
            post_absolute_url = urlparse.urljoin(response.url, post_link.strip())
            yield Request(post_absolute_url, self.handle_blog)
