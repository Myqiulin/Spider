# coding=utf-8
import urllib
import urllib2


def loadPage(word):

    url = """http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&sessionFrom=null"""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
    form_data = {
        "i": word,
        "from": "AUTO",
        "to": "AUTO",
        "smartresult": "dict",
        "client": "fanyideskweb",
        # "salt": "1500290419386",
        # "sign": "ba15a79bf95ab57646418cf337bd58ac",
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "action": "FY_BY_CL1CKBUTTON",
        "typoResult": "true",
    }
    form_data = urllib.urlencode(form_data)
    request = urllib2.Request(url, data=form_data, headers=headers)
    response = urllib2.urlopen(request)
    # read到的是一个字符串，两边有空格，需要用strip方法将两边的空格删掉
    str = response.read().strip()
    str = eval(str)["translateResult"][0][0]["tgt"]
    # 查看得知已经转换为了字典格式
    # print type(str)
    print "翻译结果为：%s"%str
if __name__ == "__main__":
    while True:
        word = raw_input("请输入您要查询的内容,退出请输入'q'：")
        if word == "q":
            break
        loadPage(word)
