import scrapy

from scrapy.loader import ItemLoader

from ..items import ZenithbankItem
from itemloaders.processors import TakeFirst


class ZenithbankSpider(scrapy.Spider):
	name = 'zenithbank'
	start_urls = ['https://www.zenithbank.com/umbraco/surface/NewsList/IndexSimple/?id=1655&recordsPerPage=999999&categoryId=&page=1']

	def parse(self, response):
		post_links = response.xpath('//div[@class="newstitle"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h2[@class="entry-title"]//text()/text()[normalize-space()]').get()
		description = response.xpath('//div[@itemprop="articleBody"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()

		item = ItemLoader(item=ZenithbankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		return item.load_item()
