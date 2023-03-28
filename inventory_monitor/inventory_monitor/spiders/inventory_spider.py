import scrapy
from inventory_monitor.items import InventoryMonitorItem

class InventorySpider(scrapy.Spider):
    name = 'inventory_spider'
    allowed_domains = ['example.com']
    start_urls = ['https://www.example.com/shop/']

    def parse(self, response):
        products = response.xpath('//div[@class="product"]')
        for product in products:
            item = InventoryMonitorItem()
            item['name'] = product.xpath('.//h3/a/text()').get()
            item['price'] = product.xpath('.//span[@class="price"]/text()').get()
            item['availability'] = product.xpath('.//p[@class="availability"]/text()').get()

            yield item

        # Pagination
        next_page = response.xpath('//a[@class="next"]/@href').get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
