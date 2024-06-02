import scrapy
import pandas as pd
class SwatchSpider(scrapy.Spider):
    name = "swatch_spider"
    allowed_domains = ["swatch.com"]
    start_urls = ["https://www.swatch.com/ru-ru/mens-watches/"]
    custom_settings = {
        'ITEM_PIPELINES': {
            '__main__.ExcelPipeline': 1
        }
    }
    def parse(self, response):
        # Получаем список всех часов на странице
        watches = response.xpath('//div[@class="product-tile"]')
        for watch in watches:
            name = watch.xpath('.//span[@class="product-name"]/text()').get().strip()
            price = watch.xpath('.//span[@class="sales-price"]/text()').get().strip()
            link = response.urljoin(watch.xpath('.//a[@class="thumb-link"]/@href').get())
            image = watch.xpath('.//img[@class="primary-image"]/@src').get()

            yield {
                'model': name,
                'description': f"Price: {price}, Link: {link}, Image: {image}"
            }
        # Пагинация
        next_page = response.xpath('//a[@class="next"]/@href').get()
        if next_page:
            yield response.follow(next_page, self.parse)
class ExcelPipeline:
    def open_spider(self, spider):
        self.items = []
    def close_spider(self, spider):
        df = pd.DataFrame(self.items)
        df.to_excel('watches.xlsx', index=False)
    def process_item(self, item, spider):
        self.items.append(item)
        return item
