from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider  # Rule
from scrapy.http.request import Request
import html2text
import time
import re
import dateutil.parser
import urlparse
from buzz_crawler.items import BuzzCrawlerItem
from markdown import markdown


class RpsSpider(CrawlSpider):
    name = 'rps'
    allowed_domains = ['www.rockpapershotgun.com']
    start_urls = ['http://www.rockpapershotgun.com/']

    def handle_blog(self, response):
        hxs = HtmlXPathSelector(response)
        item = BuzzCrawlerItem()

        item['url'] = response.url

        stringdate = hxs.select("/html/body/div[2]/div[2]/div[1]/div[1]/div[1]/div/div[1]/p[1]//text()").extract()[2]
        item['date'] = dateutil.parser.parse(stringdate)
        item['title'] = hxs.select("//div[@class='post-inner']/h2/a/text()").extract()[0]
        item['blurb'] = ""

        unprocessed_content = hxs.xpath("//div[@class='post-inner']/div[@class='entry']").extract()[0]
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        processed_content = h.handle(unprocessed_content)

        #item['content'] = markdown(processed_content)

        item['content'] = re.sub('<p>Tweet this</p>\n', '', markdown(processed_content))

        # "<p>Tweet this</p>"

        item['source'] = 'rockpapershotgun.com'
        yield item

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        posts = hxs.xpath("//div[@class='post-inner']")
        
        for post in posts:
            post_link = post.xpath("h2/a/@href").extract()[0]
            post_absolute_url = urlparse.urljoin(response.url, post_link.strip())
            yield Request(post_absolute_url, self.handle_blog)
