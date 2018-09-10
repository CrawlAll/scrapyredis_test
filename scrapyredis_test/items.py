# -*- coding: utf-8 -*-
import scrapy


class DownloadDataItem(scrapy.Item):
	user_id = scrapy.Field()
	nick_name = scrapy.Field()
	city = scrapy.Field()
	comment_time = scrapy.Field()
	comment_score = scrapy.Field()
	content = scrapy.Field()