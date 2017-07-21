import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class Top100Spider(CrawlSpider):
    name = 'top100spider'
    allowed_domains = ['metrolyrics.com']
    start_urls = ['http://www.metrolyrics.com/top100.html']

    rules = (
        ##Extrae links de los top100 de todos los géneros de la página.
        Rule(LinkExtractor(allow=('top100.*\.html', ),
                           restrict_xpaths=("//*[@id=\"main-content\"]/div[1]/div/ul"))),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=('.*-lyrics\.html', ),
                           tags=["a.subtitle"],),
             callback='parse_item'),
    )

    def parse_item(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)
        item = scrapy.Item()
        # item['id'] = response.xpath('//td[@id="item_id"]/text()').re(r'ID: (\d+)')
        # item['name'] = response.xpath('//td[@id="item_name"]/text()').extract()
        # item['description'] = response.xpath('//td[@id="item_description"]/text()').extract()
        return item
