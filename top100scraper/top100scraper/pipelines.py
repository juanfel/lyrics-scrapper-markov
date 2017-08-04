# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from top100scraper.db_manager import LyricDatabase
import pylast 

class Top100ScraperPipeline(object):
    """Guarda los items en la BD"""
    def process_item(self, item, spider):
        db = LyricDatabase()
        db.connect()
        db.add_lyric(item['artist'], item['song'], item['text'])
        return item

class GetTagsPipeline(object):
    """Busca tags de los artistas en Last.fm.
    Necesita las credenciales de usuario, las cuales son obtenidas desde el spider."""
    API_KEY = '574d1c1a07bcaf2fdcf57aa75babde50'
    API_SECRET = '7fd795ca45a71f92a42b6fbbbdd8400e'

    def open_spider(self, spider):
        self.user = spider.user
        self.password = pylast.md5(spider.password)

    def process_item(self, item, spider):
        network = pylast.LastFMNetwork(api_key = self.API_KEY,
                                       api_secret = self.API_SECRET,
                                       username = self.user,
                                       password_hash = self.password)

        artist = network.get_artist(item['artist'])
        song = network.get_track(item['artist'], item['song'])
        tags = song.get_top_tags()
        print(tags)
        item['tags'] = tags
        return item
