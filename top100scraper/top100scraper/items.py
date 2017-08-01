# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Top100ScraperItem(scrapy.Item):
    """Modelo para una canción obtenida"""
    artist = scrapy.Field()
    song = scrapy.Field()
    text = scrapy.Field()
