# -*- coding: utf-8 -*-
import json
import logging
import time

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

phantomjs = dict(DesiredCapabilities.PHANTOMJS)
phantomjs["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"
)
logger = logging.getLogger(__name__)

phantomjs_executable_path = "D:\\development\\phantomjs-2.1.1\\bin\\phantomjs.exe"

weibo_account_list = [
    ('caze@foxmail.com', 'XlWeI2017@'),
    ('1663926693@qq.com', 'cai1835313554000'),
]


def _login(account, password):
    """ 获取一个账号的Cookie """
    browser = None
    cookie = {}
    try:
        browser = webdriver.PhantomJS(desired_capabilities=phantomjs, executable_path=phantomjs_executable_path)
        browser.get("https://passport.weibo.cn/signin/login?entry=mweibo")
        time.sleep(2)
        # DEBUG CODE
        # browser.save_screenshot("a1.png")
        username = browser.find_element_by_xpath('//input[@id="loginName"]')
        username.clear()
        username.send_keys(account)
        psd = browser.find_element_by_xpath('//input[@type="password"]')
        psd.clear()
        psd.send_keys(password)
        # FIX IT 可能会出现验证码
        commit = browser.find_element_by_xpath('//a[@id="loginAction"]')
        commit.click()
        time.sleep(3)

        for elem in browser.get_cookies():
            cookie[elem["name"]] = elem["value"]
        logger.info("Login to the Weibo successful, acount is: %s." % account)
        return json.dumps(cookie)
    except Exception, e:
        logger.error("Login to the Weibo failed, acount is: %s, error: %s" % (account, e))
    finally:
        try:
            if not browser:
                browser.quit()
        except Exception, e:
            logger.error(e)
    return cookie


def execute_login(redis_conn=None, spider_name=None, redis_cookie=None):
    """  """
    cookie_count = 0
    for account, password in weibo_account_list:
        redis_key_cookie = redis_cookie % (spider_name, account)

        if redis_conn.get(redis_key_cookie) is None:
            cookie = _login(account, password)
            if len(cookie) > 0:
                redis_conn.set(name=redis_key_cookie, value=cookie, ex=259200)
                cookie_count += 1
        else:
            cookie_count += 1

    logger.info("Found the Weibo cookies %s, account queue is %s." % (str(cookie_count), str(len(weibo_account_list))))
