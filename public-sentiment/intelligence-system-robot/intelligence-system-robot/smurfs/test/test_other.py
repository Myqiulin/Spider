# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf8')
#
# content1 = """
# <div class="c" id="M_DqmWHkzof"><div><span class="ctt">一个睡不着的夜晚。与旧人谈新事，总会不禁由旧人追忆到旧事，虽然具体经过已经很模糊，可以自以为是大大咧咧的忘掉，但是那份感觉终究是忘不掉的。原来有些事，已经深深刻在脑海里，几乎一辈子也不会忘记。愿一切美好长留，不美好的能被岁月宽容。就这样，晚安[月亮][月亮][月亮] <a href="http://weibo.cn/sinaurl?f=w&amp;u=http%3A%2F%2Ft.cn%2F8kervWV&amp;ep=DqmWHkzof%2C2899591923%2CDqmWHkzof%2C2899591923">南京·南京森林警察学院</a> &#8203;&#8203;&#8203;</span>&nbsp;<a href="http://place.weibo.com/imgmap/poiid=B2094757D16CA0F94392&amp;center=32.106556,
# 118.9216&amp;backurl=http%253A%252F%252Fweibo.cn%252Fu%252F2899591923%253Frand%253D2965">显示地图</a></div><div><a href="http://weibo.cn/mblog/pic/DqmWHkzof?rl=0"><img src="http://ww2.sinaimg.cn/wap180/acd442f3jw1f2rzkjzwy3j20e60dwq47.jpg" alt="图片" class="ib"></a>&nbsp;<a href="http://weibo.cn/mblog/oripic?id=DqmWHkzof&amp;u=acd442f3jw1f2rzkjzwy3j20e60dwq47">原图</a>&nbsp;<a href="http://weibo.cn/attitude/DqmWHkzof/add?uid=3511818223&amp;rl=0&amp;st=ae259f">赞[5]</a>&nbsp;<a
# href="http://weibo.cn/repost/DqmWHkzof?uid=2899591923&amp;rl=0">转发[0]</a>&nbsp;<a href="http://weibo.cn/comment/DqmWHkzof?uid=2899591923&amp;rl=0#cmtfrm" class="cc">评论[0]</a>&nbsp;
# <a href="http://weibo.cn/fav/addFav/DqmWHkzof?rl=0&amp;st=ae259f">收藏</a><!---->&nbsp;<span class="ct">2016-04-10 22:51:38&nbsp;来自iPhone 6</span></div></div>
# """
#
# content = """
# <div class="c" id="M_DtvIF4SrO"><div><span class="cmt">转发了&nbsp;<a href="http://weibo.cn/206428889">張小_x</a>
# <img src="http://h5.sinaimg.cn/upload/2016/05/26/319/donate_btn_s.png" alt="M">&nbsp;的微博:</span><span class="ctt">
# 昨晚的草莓…昨晚的<a href="/n/Leah%E7%AB%A5Dou">@Leah童Dou</a> &#8203;&#8203;&#8203;</span>&nbsp;
# [<a href="http://weibo.cn/mblog/picAll/DtttErp71?rl=1">组图共9张</a>]</div><div><a href="http://weibo.cn/mblog/pic/DtttErp71?rl=0">
# <img src="http://ww2.sinaimg.cn/wap180/62aaa920jw1f3flq5zc6ij20v27cghdu.jpg" alt="图片" class="ib"></a>&nbsp;
# <a href="http://weibo.cn/mblog/oripic?id=DtttErp71&amp;u=62aaa920jw1f3flq5zc6ij20v27cghdu">原图</a>&nbsp;
# <span class="cmt">赞[3049]</span>&nbsp;<span class="cmt">原文转发[6306]</span>&nbsp;
# <a href="http://weibo.cn/comment/DtttErp71?rl=0#cmtfrm" class="cc">原文评论[953]</a>
# <!----></div><div><span class="cmt">转发理由:</span>//<a href="/n/Leah%E7%AB%A5Dou">@Leah童Dou</a>://<a href="/n/Leah%E7%AB%A5Dou-Fans">@Leah童Dou-Fans</a>:<a href="http://weibo.cn/pages/100808topic?extparam=%E7%AA%A6%E9%9D%96%E7%AB%A5%E8%8D%89%E8%8E%93%E9%9F%B3%E4%B9%90%E8%8A%82&amp;from=feed">#窦靖童草莓音乐节#</a> 认真唱歌的样子最迷人[可爱][心]&nbsp;&nbsp;<a href="http://weibo.cn/attitude/DtvIF4SrO/add?uid=3511818223&amp;rl=0&amp;st=ae259f">赞[0]</a>&nbsp;<a
# href="http://weibo.cn/repost/DtvIF4SrO?uid=2899591923&amp;rl=0">转发[0]</a>&nbsp;<a href="http://weibo.cn/comment/DtvIF4SrO?uid=2899591923&amp;rl=0#cmtfrm" class="cc">评论[0]</a>&nbsp;<a href="http://weibo.cn/fav/addFav/DtvIF4SrO?rl=0&amp;st=ae259f">收藏</a><!---->&nbsp;<span class="ct">2016-05-01 14:42:41&nbsp;来自iPhone 6</span></div></div>
#
# """
#
# soup = BeautifulSoup(content, "lxml")
# tags = soup.find_all(attrs={"class": "ctt"})
# for tag in tags:
#     strs = tag.strings
#     for str in strs:
#         print str

# print unicode("你好","utf-8")
# conn = mysql.connector.connect(host="localhost",
#                                port="3306",
#                                user="root",
#                                password="root",
#                                database="db_weibo",
#                                charset="utf8")
# sql = """
# select id,create_time  from tb_tweets where length(create_time) = 11 and create_time not like '%分钟前'
# """
#
# update_sql = "update tb_tweets set create_time = %s where id = %s "
# cursor = conn.cursor()
# util = CommonUtil()
# cursor.execute(sql)
# data = tuple(cursor)
# cursor.close()
#
# cursor = conn.cursor()
# for (id, create_time) in data:
#     try:
#         params = (util.parse_time(str(create_time)), id)
#         cursor.execute(update_sql, params)
#         conn.commit()
#     except Exception, e:
#         print e
#
#
# cursor.close()
# conn.close()

print
