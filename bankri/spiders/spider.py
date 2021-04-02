import scrapy

from scrapy.loader import ItemLoader

from ..items import BankriItem
from itemloaders.processors import TakeFirst


class BankriSpider(scrapy.Spider):
	name = 'bankri'
	start_urls = ['https://www.bankri.com/aboutus/articles/']

	def parse(self, response):
		post_links = response.xpath('//span[@class="links"]')
		for post in post_links:
			url = post.xpath('./a/@href').get()
			date = post.xpath('./span/text()').get()
			yield response.follow(url, self.parse_post, cb_kwargs={'date': date})

	def parse_post(self, response, date):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@id="subpage-content"]//text()[normalize-space() and not(ancestor::h1)]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()

		item = ItemLoader(item=BankriItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
