# -*- coding: utf-8 -*-

__author__ = "Johnny"

from lxml import html
import re
import requests
import json
from write2db import Write2DB
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

"""
weibo_url = "https://m.weibo.cn/api/container/getIndex?containerid=1076031913839234&page=2"

comment_url = "https://m.weibo.cn/api/comments/show?id=4176819562975925&page=1"

"""
class Crawl_weibo(object):

	def __init__(self):
		self.headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:57.0) Gecko/20100101 Firefox/57.0"}
		self.pattern = re.compile(r'^<(.*?)>')

	def get_weibo(self, id, page):
		"""获取微博详情"""
		# 根据id和page获取用户发过的微博
		weibo_url = "https://m.weibo.cn/api/container/getIndex?containerid=107603{}&page={}".format(id, page)
		# 获得相应
		res = requests.get(url=weibo_url, headers=self.headers)
		# 转换为字典
		res_dict = json.loads(res.text)
		cards = res_dict.get("cards")  # 拿到单个请求的微博详情总数
		if cards == []:
			return 0
		for card in cards:
			page = 1
			print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>获取微博信息")
			# 判断是微博还是广告，card_type为9就是微博
			if card.get("card_type") == 9:
				single_blog = card.get("mblog")  # 一条微博详情,包含以下内容
				content = single_blog.get("text", "'null'")  # 微博内容
				if not content:
					content = ''
				tree = html.fromstring(content)
				content = tree.xpath('string(.)')
				content = str(re.sub(self.pattern, '', content))
				create_time = str(single_blog.get("created_at", "'null'"))  # 发布时间
				repost_count = str(single_blog.get("reposts_count", "'null'"))  # 转发数量
				comment_count = str(single_blog.get("comments_count", "'null'"))  # 评论数量
				attitude_count = str(single_blog.get("attitudes_count", "'null'"))  # 点赞数
				device = str(single_blog.get("source"))  # 发布设备
				if device == "":
					device = "'未知'"
				blog_id = str(single_blog.get("id", "null")) # 拿到该条微博ID
				Write2DB.write2blog(content,create_time, repost_count, comment_count, attitude_count,device,blog_id)
				count = 1
				while True:
					print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<获取第{}页的评论请求".format(count))
					exec_if = self.get_comment(blog_id, page)
					count+=1
					page += 1
					print(count,page)
					if exec_if == 0:
						print("<<<<<<<<<<<<<<<<<<没有你要的评论页面了>>>>>>>>>>>>>>>>>>>>")
						break
		# print(type(res_dict))

	def get_comment(self, id, page):
		"""获取当前微博评论详情"""
		comment_url = "https://m.weibo.cn/api/comments/show?id={}&page={}".format(id, page)
		# print(comment_url)
		res = requests.get(url=comment_url, headers=self.headers)
		res_dict = json.loads(res.text)
		if res_dict.get("ok") == 0:
			return 0
		else:
			datas = res_dict.get("data")  # 拿到单个请求的所有评论
			for i,data in enumerate(datas):
				print("<<<<<<<<<<<<<<<<<<第{}条评论>>>>>>>>>>>>>>>>>>>".format(i+1))
				content = data.get("text")  # 获取评论内容
				tree = html.fromstring(content)
				content = tree.xpath('string(.)')
				content = str(re.sub(self.pattern, '', content))
				user_name = str(data.get("user").get("screen_name"))  # 获取评论用户昵称
				create_time = str(data.get("created_at"))  # 获取评论时间
				attitude_count = str(data.get("like_counts"))  # 获取点赞数
				device = str(data.get("source"))  # 获取发布设备
				Write2DB.write2comment(user_name,content,create_time,attitude_count,device,id)

	def exec_spider(self):
		"""执行程序"""
		page = 1
		user_id = input("请输入用户ID：")
		while True:
			exec_if = self.get_weibo(str(user_id), page)
			page+=1
			if exec_if == 0:
				print("<<<<<<<<<<<<<<<<<<没有你要的微博页面了>>>>>>>>>>>>>>>>>>>>")
				break
			
if __name__ == "__main__":
	spider = Crawl_weibo()
	spider.exec_spider()






