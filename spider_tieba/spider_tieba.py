# coding=utf-8

# 对url进行编码
import urllib
# 执行Http请求
import urllib2


def loadPage(url, fileName):
    "加载页面"
    print "正在下载"+fileName
    user_agent = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
    request = urllib2.Request(url, headers=user_agent)
    try:
        response = urllib2.urlopen(request)
        return response.read()
    except Exception as e:
        print e


def writePage(html, fileName):
    "用于将爬取的信息写入到磁盘"
    print "正在写入"+fileName
    with open(fileName, "w") as f:
        f.write(html)


def tiebaSpider(url, startPage, endPage):
    "用于处理爬取过程,构造url"
    for page in range(startPage, endPage+1):
        pn = (page - 1)*50
        keyWord = urllib.urlencode({"pn": pn})
        fullUrl = url+"&"+keyWord
        fileName = "第"+str(page)+"页.html"
        html = loadPage(fullUrl, fileName)
        writePage(html, fileName)

if __name__ == "__main__":
    name = raw_input("请输入你想要爬取的贴吧：")
    startPage = int(raw_input("请输入你想要爬取的起始页："))
    endPage = int(raw_input("请输入你想要爬取的终止页："))
    base_url = "http://tieba.baidu.com/f?"
    keyWord = {"kw": name}
    kw = urllib.urlencode(keyWord)
    url = base_url + kw
    tiebaSpider(url, startPage, endPage)