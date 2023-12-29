# Scrapy settings for books project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "books"

SPIDER_MODULES = ["books.spiders"]
NEWSPIDER_MODULE = "books.spiders"

#ITEM_PIPELINES = {
    #"books.pipelines.BooksPipeline": 300,
#    "books.pipelines.SaveDataToPostgres": 400,
# }

ITEM_PIPELINES = {
    "scrapy.pipelines.images.ImagesPipeline": 1,
    #"books.pipelines.BookImagesPipeline":2,
    "books.pipelines.BooksPipeline": 3,
    "books.pipelines.SaveDataToPostgres": 4,
}
IMAGES_STORE = "images/"

# FEEDS = {"booksdata.json": {"format": "json", "overwrite": True}}


# Obey robots.txt rules
ROBOTSTXT_OBEY = True
