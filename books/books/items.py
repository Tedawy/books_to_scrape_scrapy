# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass


class BooksItemInfo(scrapy.Item):
    
    title = scrapy.Field()
    category =  scrapy.Field()
    price = scrapy.Field()
    #product_description = scrapy.Field()
    product_type = scrapy.Field()
    price_excl_tax = scrapy.Field()
    price_incl_tax = scrapy.Field()
    tax = scrapy.Field()
    availability = scrapy.Field()
    number_of_reviews = scrapy.Field()
    stars = scrapy.Field()