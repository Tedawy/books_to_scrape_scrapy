from typing import Iterable
import scrapy
from books.items import BooksItemInfo

# from scrapy.http import Request


class BookSpider(scrapy.Spider):
    name = "book"

    def start_requests(self):
        URL = "https://books.toscrape.com"
        yield scrapy.Request(url=URL, callback=self.parse)

    def parse(self, response):
        books = response.css("article.product_pod")
        for book in books:
            book_page = book.css("h3 a::attr(href)").get()
            if book_page:
                yield response.follow(book_page, callback=self.parse_book_apge)
        
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        

    def parse_book_apge(self, response):
        book_info = BooksItemInfo()
        table_info = response.css("table tr")

        # Book Info
        book_info["title"] = response.css(".product_main h1::text").get()
        book_info["category"] = response.xpath(
            "//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()"
        ).get()
        book_info["price"] = response.css("p.price_color ::text").get()
        """
        book_info["product_description"] = response.xpath(
            "//div[@id='product_description']/following-sibling::p/text()"
        ).get()
        """
        book_info["product_type"] = table_info[1].css("td ::text").get()
        book_info["price_excl_tax"] = table_info[2].css("td ::text").get()
        book_info["price_incl_tax"] = table_info[3].css("td ::text").get()
        book_info["tax"] = table_info[4].css("td ::text").get()
        book_info["availability"] = table_info[5].css("td ::text").get()
        book_info["number_of_reviews"] = table_info[6].css("td ::text").get()
        book_info["stars"] = response.css("p.star-rating").attrib["class"]

        # Books images
        book_info["image_urls"] = [
            response.urljoin(response.css(".active img::attr(src)").get())
        ]

        yield book_info
