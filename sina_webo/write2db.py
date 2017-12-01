# -*- coding: utf-8 -*-

from settings import *
from pymysql import *

class Write2DB(object):
	"""
	将抓取内容写入到数据库
	"""
	count = 1
	count_comment = 1
	def __init__(self):
		pass
		
	@staticmethod
	def write2blog(content,create_time, repost_count, comment_count, attitude_count,device,blog_id):
		"""写入到blogs数据表"""
		print("i am comming into {} 第{}次".format(TABLE1, Write2DB.count))
		Write2DB.count+=1
		# 创建连接
		conn = connect(host=POST, port=PORT, database=DB_NAME, user=USER, password=PASSWORD, charset='utf8mb4')
		# 创建cursor对象
		cs = conn.cursor()
		cs.execute('SET NAMES utf8mb4;') 
		cs.execute('SET CHARACTER SET utf8mb4;')
		cs.execute('SET character_set_connection=utf8mb4;')
		# table = TABLE1
		
		sql = '''insert into {}(blog,create_time,repost_count,comment_count,attitude_count,device,blog_id) values(%s,%s,%s,%s,%s,%s,%s)'''.format(TABLE1)
		params = [content,create_time, repost_count, comment_count, attitude_count,device,blog_id]
		cs.execute(sql, params)
		cs.close()
		conn.commit()
		conn.close()

	@staticmethod
	def write2comment(user_name,content,create_time,attitude_count,device,id):
		"""写入到comments表"""
		print("i am comming into {} 第{}次".format(TABLE2, Write2DB.count_comment))
		conn = connect(host=POST, port=PORT, database=DB_NAME, user=USER, password=PASSWORD, charset='utf8mb4')
		# 创建cursor对象
		cs = conn.cursor()
		cs.execute('SET NAMES utf8mb4;') 
		cs.execute('SET CHARACTER SET utf8mb4;')
		cs.execute('SET character_set_connection=utf8mb4;')
		sql = '''insert into {}(user_name,comment,create_time,attitude_count,device,pid) values(%s,%s,%s,%s,%s,%s)'''.format(TABLE2)
		params = [user_name, content, create_time, attitude_count,device,id]
		Write2DB.count_comment+=1
		cs.execute(sql, params)
		cs.close()
		conn.commit()
		conn.close()
