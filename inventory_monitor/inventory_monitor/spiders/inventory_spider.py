import scrapy
from inventory_monitor.items import InventoryMonitorItem

class InventorySpider(scrapy.Spider):
    name = 'inventory_spider'
    allowed_domains = ['example.com']
    start_urls = ['https://www.amazon.com/s?k=gaming+headsets&pd_rd_r=a63f202e-7e95-4176-95f0-caf628c482cf&pd_rd_w=7hFdI&pd_rd_wg=7wVvr&pf_rd_p=12129333-2117-4490-9c17-6d31baf0582a&pf_rd_r=PDM5GCMDAJT1ZG8RY9Q2&ref=pd_gw_unk']

    def parse(self, response):
        products = response.xpath('//<h2 class="a-size-mini a-spacing-none a-color-base s-line-clamp-2">')
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
