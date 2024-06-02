import scrapy


class SwatchSpider(scrapy.Spider):
    name = "swatch_spider"
    allowed_domains = ["swatch.com"]
    start_urls = ["https://www.swatch.com/ru-ru/mens-watches/"]

    def parse(self, response):
        # Получаем список всех часов на странице
        watches = response.xpath('//div[@class="product-tile"]')

        for watch in watches:
            yield {
                'name': watch.xpath('.//span[@class="product-name"]/text()').get(),
                'price': watch.xpath('.//span[@class="sales-price"]/text()').get(),
                'link': watch.xpath('.//a[@class="thumb-link"]/@href').get(),
                'image': watch.xpath('.//img[@class="primary-image"]/@src').get(),
            }

        # Пагинация
        next_page = response.xpath('//a[@class="next"]/@href').get()
        if next_page:
            yield response.follow(next_page, self.parse)
