# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re
import psycopg2
from scrapy.pipelines.images import ImagesPipeline


class BooksPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Remove £ from all columns
        price_keys = ["price", "price_excl_tax", "price_incl_tax", "tax"]
        for price in price_keys:
            value = adapter.get(price)
            value = value.replace("£", "")
            adapter[price] = float(value)

        # availability
        avail = adapter.get("availability")
        value = re.findall(r"\d+", avail)
        adapter["availability"] = value[0]

        # stars
        stars = adapter.get("stars")
        rate = stars.split()[-1]
        rates = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
        adapter["stars"] = rates.get(rate, None)

        return item


class SaveDataToPostgres:
    def __init__(self) -> None:
        try:
            self.conn = psycopg2.connect(
                database="web-scraping",
                user="user",
                host="localhost",
                password="password",
                port=5432,
            )
            # create cursor, used to execute commands
            self.cur = self.conn.cursor()

            # create books table if not exist
            self.cur.execute(
                """
                CREATE TABLE IF NOT EXISTS books(
                    id SERIAL PRIMARY KEY,
                    title TEXT,
                    category VARCHAR(255), 
                    price FLOAT,
                    product_type VARCHAR(255),
                    price_excl_tax DECIMAL,
                    price_incl_tax DECIMAL,
                    tax DECIMAL,
                    availability INT,
                    number_of_reviews INT,
                    stars INT
                )     
                """
            )
        except Exception as e:
            print(f"Error initializing database: {e}")

    def process_item(self, item, spider):
        try:
            self.cur.execute(
                """
                INSERT INTO books(
                    title,
                    category,
                    price,
                    product_type,
                    price_excl_tax,
                    price_incl_tax,
                    tax,
                    availability,
                    number_of_reviews,
                    stars    
                )
                VALUES (
                    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s
                )
                """,
                (
                    item["title"],
                    item["category"],
                    item["price"],
                    item["product_type"],
                    item["price_excl_tax"],
                    item["price_incl_tax"],
                    item["tax"],
                    item["availability"],
                    item["number_of_reviews"],
                    item["stars"],
                ),
            )

            self.conn.commit()
        except Exception as e:
            print(f"Error processing item: {e}")

        return item

    def close_spider(self, spider):
        try:
            # close cursor and connection to the database
            self.cur.close()
            self.conn.close()
        except Exception as e:
            print(f"Error closing database connection: {e}")


