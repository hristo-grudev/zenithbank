import scrapy


class ZenithbankItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
