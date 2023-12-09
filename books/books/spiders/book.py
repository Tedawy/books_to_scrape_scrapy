from typing import Iterable
import scrapy
#from scrapy.http import Request


class BookSpider(scrapy.Spider):
    name = "book"
    
    def start_requests(self):
        URL = 'https://books.toscrape.com'
        yield scrapy.Request(url= URL , callback= self.parse)

    def parse(self, response):
            for article in response.css("article.product_pod"):
                yield{
                    'title' : article.css("h3 > a::attr(title)").get(),
                    'price' : article.css('.price_color::text').extract_first(),
                    'rating' : article.css('p.star-rating::attr(class)').re_first('star-rating (.*)')

                }
                
            next_page = response.css('li.next a::attr(href)').get()
            if next_page:
                yield response.follow(next_page, callback=self.parse)
            'book_img': article.css("img::attr(src)").get()

            
        

