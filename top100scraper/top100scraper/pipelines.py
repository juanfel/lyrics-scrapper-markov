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
    SHARED_SECRET = '7fd795ca45a71f92a42b6fbbbdd8400e'
    
    def process_item(self, item, spider):
        return spider
