# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BooksDetailsPipeline:
    def process_item(self, item, spider):
        return item


class BookPricePipeline:
    """
    Pipeline to process price, remove the pound sign '£' and convert into numerical type.
    """
    def process_item(self, item, spider):
        price_str = item.get("price")
        price_numerical = float(price_str[1:])

        spider.logger.info("Removing the '£' sign and changing the price to numerical type.")
        item["price"] = price_numerical

        return item
