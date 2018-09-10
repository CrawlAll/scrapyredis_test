# -*- coding: utf-8 -*-
import scrapy
import json
from datetime import datetime
from scrapyredis_test.items import DownloadDataItem


# 抓取 邪不压正的影评
class XbyzMovieSpider(scrapy.Spider):
	name = 'xbyz_movie'
	allowed_domains = ['maoyan.com']
	custom_settings = {'LOG_LEVEL': "INFO"}

	def start_requests(self):
		base_urls = 'http://m.maoyan.com/mmdb/comments/movie/248566.json?_v_=yes&offset='
		for offset_num in range(1, 1001):
			url = base_urls + str(offset_num)
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		self.logger.info(f"本次请求url为 {response.url}.......................")
		item = DownloadDataItem()
		text = response.text

		data_list = json.loads(text).get('cmts')
		for data in data_list:
			user_id = data['userId']
			nick_name = data['nickName']
			city = data['cityName']
			time = data['time']
			comment_time = datetime.strptime(time, "%Y-%m-%d %H:%M")
			comment_score = data['score']
			content = data['content']

			for field in item.fields:
				item[field] = eval(field)
			yield item
