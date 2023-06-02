# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ShienProductItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    image = scrapy.Field()
    price = scrapy.Field()
    source = scrapy.Field()
    pass
