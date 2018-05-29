# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NeteasemusicItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class MusicItem(scrapy.Item):
    # define the fields for your item here like:
    # 我们保存歌曲的id
    id = scrapy.Field()
    artist = scrapy.Field()
    album = scrapy.Field()
    music = scrapy.Field()
    comments = scrapy.Field()
