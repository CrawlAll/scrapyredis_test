# -*- coding: utf-8 -*-
import user_agent
import requests


class RandomUserAgentMiddleware(object):
	def process_request(self, request, spider):
		userAgent = user_agent.generate_user_agent()
		request.headers.setdefault("User-Agent", userAgent)


class RandomProxyMiddleware(object):
	def __init__(self, proxy_url):
		self.proxy_url = proxy_url

	@classmethod
	def from_crawler(cls, crawler):
		settings = crawler.settings
		return cls(
			proxy_url=settings.get('PROXY_URL')
		)

	def get_random_proxy(self):
		try:
			response = requests.get(self.proxy_url)
			if response.status_code != 200:
				return False
			proxy = response.text
			return proxy
		except requests.ConnectionError:
			return False

	def process_request(self, request, spider):
		if request.meta.get('retry_times'):
			proxy = self.get_random_proxy()
			if proxy:
				uri = 'https://{proxy}'.format(proxy=proxy)
				spider.logger.info('使用代理 {proxy}'.format(proxy=proxy))
				request.meta['proxy'] = uri
			else:
				spider.logger.error('使用代理异常')
