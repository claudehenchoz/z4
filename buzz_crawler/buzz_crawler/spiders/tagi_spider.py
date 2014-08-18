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


class TagiSpider(CrawlSpider):
    name = 'tagi'
    allowed_domains = ['www.tagesanzeiger.ch']
    start_urls = ['http://www.tagesanzeiger.ch/']

    def handle_blog(self, response):
        hxs = HtmlXPathSelector(response)
        item = BuzzCrawlerItem()

        print(response)

        item['url'] = response.url

        stringdate = hxs.xpath("//span[@class='publishedDate']/text()").extract()
        item['date'] = dateutil.parser.parse(stringdate[0].replace("(Erstellt: ","").replace("Uhr)",""))
        item['title'] = hxs.xpath("//div[@id='article']/h1/text()").extract()[0].strip()
        item['blurb'] = hxs.xpath("//div[@id='article']/h3/text()").extract()[0].strip()

        print "*"*60
        #print(item['title'])
        print "*"*60
        #print(item['date'])
        print "*"*60
        #print(item['blurb'])
        print "*"*60

        unprocessed_content = hxs.xpath("//div[@id='mainContent']").extract()[0]
        #print(unprocessed_content)

        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True

        processed_content = h.handle(unprocessed_content)
        #processed_content = html2text.html2text(unprocessed_content)
        #print(processed_content)
        print "*"*60

        item['content'] = markdown(processed_content)

        item['source'] = 'tagesanzeiger.ch'

        #print dir(hxs.select("//div[@class='post-inner']/div[@class='entry']"))

        yield item

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        #prev = hxs.select("//div[@class='content-nav']/a[@rel='next']/@href").extract()
        #prev_page_link = urlparse.urljoin("http://radar.oreilly.com/tim/", prev[0])
        #yield Request(prev_page_link, self.parse)
        posts = hxs.xpath("//div[@class='featureStory standard']")
        #print(posts)
        
        for post in posts:
            print(post.xpath("h3/a/@href").extract())
            post_link = post.xpath("h3/a/@href").extract()[0]

            post_absolute_url = urlparse.urljoin(response.url, post_link.strip())

            yield Request(post_absolute_url, self.handle_blog)
