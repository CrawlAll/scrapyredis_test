# -*- coding: utf-8 -*-
import pymysql


class DownloadDataPipeline(object):
	def __init__(self, host, dbname, user, pwd, port):
		self.host = host
		self.dbname = dbname
		self.user = user
		self.pwd = pwd
		self.port = port

	@classmethod
	def from_crawler(cls, crawler):
		return cls(
			host=crawler.settings.get('MYSQL_HOST'),
			dbname=crawler.settings.get('MYSQL_DBNAME'),
			user=crawler.settings.get('MYSQL_USER'),
			pwd=crawler.settings.get('MYSQL_PASSWD'),
			port=crawler.settings.get('MYSQL_PORT')
		)

	def open_spider(self, spider):
		self.connect = pymysql.connect(host=self.host, db=self.dbname, user=self.user, passwd=self.pwd, port=self.port,
								  charset='utf8mb4', use_unicode=True)
		self.cursor = self.connect.cursor()

	def process_item(self, item, spider):
		upsertSql = """INSERT INTO xbyz_movie(user_id, nick_name, city, comment_time, comment_score, content) \
VALUES (%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE content=%s, city=%s, comment_time=%s, comment_score=%s, content=%s"""
		upsertParams = (
			item['user_id'], item['nick_name'], item['city'], item['comment_time'], item['comment_score'],
			item['content'],
			item['nick_name'], item['city'], item['comment_time'], item['comment_score'], item['content'])
		self.cursor.execute(upsertSql, upsertParams)
		self.connect.commit()
		return item

	def close_spider(self, spider):
		self.connect.close()
