import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import top100scraper.items

class Top100Spider(CrawlSpider):
    name = 'top100spider'
    allowed_domains = ['metrolyrics.com']
    start_urls = ['http://www.metrolyrics.com/top100.html']

    rules = (
        ##Extrae links de los top100 de todos los géneros de la página.
        Rule(LinkExtractor(allow=('top100.*\.html', ),
                           restrict_xpaths=("//*[@id=\"main-content\"]/div[1]/div/ul"))),
        ##Obtiene los links de los autores
        Rule(LinkExtractor(allow=('.*-lyrics\.html', ),
                           restrict_css=("#main-content > div.grid_8 > div > div > div.song-list.clearfix > ul.song-list.grid_4.alpha > li > span.artist > a"))
             ),
        ##Obtiene paginas extra
        # Rule(LinkExtractor(allow=('.*-alpage-.*'))),

        ##Obtiene letras
        Rule(LinkExtractor(allow=('.*-lyrics-.*', ),
                           restrict_css=("#popular > div > table")),
             callback='parse_lyric')
    )

    def __init__(self, user='', password = '', *args, **kwargs):
        """Necesita obtener los datos de la cuenta de last.fm"""
        if (password == '' or password == None or
           user == '' or user == None):
               raise Exception(ValueError)
        
        super(Top100Spider, self).__init__(*args, **kwargs)
        self.password = password
        self.user = user

    def parse_lyric(self, response):
        """Prepara las letras para ingresarlas a la base de datos"""
        artist = response.css('#mantle_skin > div.banner-wrap > div.banner > div.banner-heading > h2 > a::text ').extract_first()
        song = response.css('#mantle_skin > div.banner-wrap > div.banner > div.banner-heading > h1::text').extract_first()
        text = response.xpath('//*[@id="lyrics-body-text"]/p/text()').extract()
        item = top100scraper.items.Top100ScraperItem(artist = artist, song = song, text = text)

        return item
