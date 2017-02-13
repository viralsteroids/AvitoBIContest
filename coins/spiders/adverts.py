from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from scrapy.loader import ItemLoader
from coins.items import CoinsItem

class AdvertsSpider(CrawlSpider):
    name = 'adverts'
    allowed_domains = ['avito.ru']
    stations_numbers = [1, 2, 3, 4, 151, 2135, 5, 148, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 2145, 215, 18, 19, 20,
                        1010, 149, 127, 1012, 2155, 22, 21, 23, 24, 25, 26, 27, 1003, 28, 152, 29, 2146, 30, 31, 32, 33,
                        2001, 34, 2143, 217, 35, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 2151, 47, 48, 49, 50, 51, 52,
                        53, 54, 55, 56, 57, 58, 59, 2142, 2144, 60, 61, 62, 2002, 63, 64, 65, 1004, 66, 1001, 67, 1002,
                        68, 69, 70, 71, 2133, 72, 73, 17, 74, 75, 76, 77, 78, 79, 80, 82, 81, 36, 83, 84, 85, 86, 87,
                        88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 2136, 100, 101, 102, 2149, 103, 104, 2150, 105,
                        106, 107, 108, 1005, 109, 110, 111, 2147, 112, 1007, 214, 113, 114, 115, 116, 117, 118, 119,
                        120, 2152, 121, 122, 2148, 1006, 123, 124, 125, 126, 128, 1011, 1009, 1008, 129, 130, 131, 2154,
                        132, 133, 134, 135, 136, 137, 138, 139, 140, 216, 141, 142, 143, 144, 145, 146, 147]
    start_urls = ['https://www.avito.ru/moskva/kollektsionirovanie/monety?metro=' + str(station_number)
                  for station_number in stations_numbers]

    rules = (
        Rule(LinkExtractor(restrict_xpaths=r'//a[contains(@class, "pagination-page js-pagination-next")]')),
        Rule(LinkExtractor(restrict_xpaths=r'//a[contains(@class, "item-description-title-link")]'),
             callback='parse_item'),
    )

    def parse_item(self, response):

        il = ItemLoader(item=CoinsItem(), response=response)

        il.add_xpath('title', '//span[contains(@class, \'title-info-title-text\')]/text()')
        il.add_xpath('description', '//div[contains(@class, \'item-description-text\')]/*/text()')
        il.add_value('url', response.url)

        return il.load_item()
