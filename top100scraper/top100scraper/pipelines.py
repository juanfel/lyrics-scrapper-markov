# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from top100scraper.db_manager import LyricDatabase

class Top100ScraperPipeline(object):
    """Guarda los items en la BD"""
    def process_item(self, item, spider):
        db = LyricDatabase()
        db.connect()
        db.add_lyric(item['artist'], item['song'], item['text'])
        return item
