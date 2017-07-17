# coding=utf-8

import urllib2
import urllib


def loadPage(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
    print "开始写入"
    # 发出request请求
    request = urllib2.Request(url, headers=headers)
    # 服务器相应
    response = urllib2.urlopen(request)
    return response.read()
def writePage(content):
    """将爬取的文件写入磁盘"""
    with open("movie.json","w") as f:
        f.write(content)
    print "写入完成"
if __name__ == "__main__":
    film_type = raw_input("请输入您要查看的电影类型：")
    film_total = raw_input("请输入您想要下载的个数:")
    url = """https://movie.douban.com/j/chart/top_list?"""
    url_other = {
        "type" : film_type,
        "interval_id" : "100:90",
        "action" : "",
        "start" : "0",
        "limit" : film_total,
    }
    url_other = urllib.urlencode(url_other)
    full_url = url + url_other
    movie_json = loadPage(full_url)
    writePage(movie_json)

