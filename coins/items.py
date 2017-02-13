# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.loader.processors import Join, MapCompose, TakeFirst

from scrapy.item import Item, Field

class CoinsItem(Item):
    title = Field(output_processor=TakeFirst())
    description = Field(output_processor=Join())
    date = Field()
    url = Field(output_processor=TakeFirst())
