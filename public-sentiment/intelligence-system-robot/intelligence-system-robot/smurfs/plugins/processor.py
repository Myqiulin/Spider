# -*- coding: utf-8 -*-
import base64
import logging
import random

import redis
from scrapy.core.downloader.handlers.http11 import TunnelError
from scrapy.exceptions import NotConfigured
from scrapy.utils.response import response_status_message
from twisted.internet import defer
from twisted.internet.error import TimeoutError, DNSLookupError, \
    ConnectionRefusedError, ConnectionDone, ConnectError, \
    ConnectionLost, TCPTimedOutError
from twisted.web.client import ResponseFailed

from smurfs.util.proxy_client import choice_proxy
from smurfs.util.user_agents import agents
from smurfs.util.weibo_cookies import execute_login

logger = logging.getLogger(__name__)


class ProcessorMiddleware(object):
    """
    下载处理器：
    * 每次请求都会带上代理、UserAgent，代理IP3分钟更新一个；
    * 如果是爬取微博则带上Cookies，其他情况不带；
    * 如果下载过程出现指定错误则尝试重试3次，重试过程中会更换一个新的代理IP，并且记录日志，多次失败将丢弃本次请求。
    """

    EXCEPTIONS_TO_RETRY = (defer.TimeoutError, TimeoutError, DNSLookupError,
                           ConnectionRefusedError, ConnectionDone, ConnectError,
                           ConnectionLost, TCPTimedOutError, ResponseFailed,
                           IOError, TunnelError)

    def __init__(self, settings, crawler):
        if not settings.getbool("PROCESSOR_ENABLED"):
            raise NotConfigured
        self.max_retry_times = settings.getint("PROCESSOR_RETRY_TIMES")
        self.retry_http_codes = set(int(x) for x in settings.getlist("PROCESSOR_RETRY_HTTP_CODES"))
        self.priority_adjust = settings.getint("PROCESSOR_RETRY_PRIORITY_ADJUST")
        self.proxy_enabled = settings.getbool("PROCESSOR_PROXY_ENABLED")
        self.proxy_user = settings.get("PROCESSOR_PROXY_USER")
        self.proxy_pwd = settings.get("PROCESSOR_PROXY_PWD")
        self.proxy_server = settings.get("PROCESSOR_PROXY_SERVER")
        self.proxy_one = settings.get("RDK_PROXY_ONE")
        self.proxy_queue = settings.get("RDK_PROXY_QUEUE")
        # for weibo spider setting
        self.cookie_queue = settings.get("RDK_COOKIE_QUEUE")

        self.conn = redis.StrictRedis(host=crawler.settings.get("REDIS_HOST"),
                                      port=crawler.settings.get("REDIS_PORT"),
                                      encoding=crawler.settings.get("REDIS_ENCODING", "utf-8"),
                                      db=0)

        if crawler.spider.name == "weibo":
            execute_login(redis_conn=self.conn, spider_name=crawler.spider.name, redis_cookie=self.cookie_queue)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler)

    def process_exception(self, request, exception, spider):
        logger.error("Processor catch a exception: %s, spider name: %s.", exception, spider.name)
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) \
                and not request.meta.get("dont_retry", False):
            return self._retry(request, exception, spider)

    def proxy_setting(self, request, spider, flush_next=False):
        try:
            proxy_ip = choice_proxy(redis_conn=self.conn,
                                    flush_next=flush_next,
                                    redis_proxy_queue=self.proxy_queue,
                                    redis_proxy_one=self.proxy_one,
                                    proxy_server=self.proxy_server)
            if proxy_ip:
                request.meta["Proxy"] = "http://%s" % proxy_ip
                proxy_user_pass = "%s:%s" % (self.proxy_user, self.proxy_pwd)
                encoded_user_pass = base64.encodestring(proxy_user_pass)
                request.headers["Proxy-Authorization"] = "Basic " + encoded_user_pass
        except Exception, e:
            logger.error("Processor proxy setting error: %s, spider name: %s.", e, spider.name)

    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent
        if self.proxy_enabled:
            self.proxy_setting(request=request, spider=spider)

    def process_response(self, request, response, spider):
        if request.meta.get("dont_retry", False):
            return response
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        return response

    def _retry(self, request, reason, spider):
        retries = request.meta.get("retry_times", 0) + 1

        if retries <= self.max_retry_times:
            logger.warn("Processor retrying %(request)s (failed %(retries)d times): %(reason)s",
                        {"request": request, "retries": retries, "reason": reason},
                        extra={"spider": spider})
            retryreq = request.copy()
            retryreq.meta["retry_times"] = retries
            if self.proxy_enabled:
                self.proxy_setting(request=retryreq, spider=spider, flush_next=True)
            retryreq.dont_filter = True
            retryreq.priority = request.priority + self.priority_adjust

            return retryreq
        else:
            logger.warn("Gave up retrying %(request)s (failed %(retries)d times): %(reason)s",
                        {"request": request, "retries": retries, "reason": reason},
                        extra={"spider": spider})
