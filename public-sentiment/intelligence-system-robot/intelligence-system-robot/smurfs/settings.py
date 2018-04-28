# -*- coding: utf-8 -*-
# Robot setting
BOT_NAME = "smurfs"
SPIDER_MODULES = ["smurfs.spiders"]
NEWSPIDER_MODULE = "smurfs.spiders"
SCHEDULER = "smurfs.scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "smurfs.scrapy_redis.dupefilter.RedisDupeFilter"
ROBOTSTXT_OBEY = False
COMPRESSION_ENABLED = True
CONCURRENT_ITEMS = 200
CONCURRENT_REQUESTS = 32
DOWNLOAD_TIMEOUT = 5
DOWNLOAD_DELAY = 4
FEED_EXPORT_ENCODING = "utf-8"
DOWNLOADER_MIDDLEWARES = {
    "scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware": 100,
    "smurfs.plugins.processor.ProcessorMiddleware": 101,
}
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
}
EXTENSIONS = {
    "smurfs.plugins.metrics.SpiderMetrics": 500,
}
ITEM_PIPELINES = {
    "smurfs.pipeline.pipelines.TutorialPipeline": 303,
    # "smurfs.pipeline.database.DBPipeline": 300,
    # "smurfs.pipeline.message.ElasticsearchPipeline": 301,
    # "smurfs.pipeline.storage.HBasePipeline": 302,
    # 'smurfs.pipeline.message_kafka.KafkaPipeline': 304,
}
HTTPCACHE_ENABLED = False
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = "httpcache"
AUTOTHROTTLE_ENABLED = False
LOG_LEVEL = "DEBUG"
REDIRECT_ENABLED = True
REDIRECT_MAX_TIMES = 5
COOKIES_ENABLED = False
RETRY_ENABLED = False
TELNETCONSOLE_ENABLED = False
CLOSESPIDER_ERRORCOUNT = 10

# Redis server node setting
REDIS_HOST = "10.211.54.227"
REDIS_PORT = 6379
REDIS_ENCODING = "utf-8"
REDIS_SOCKET_TIMEOUT = 3
REDIS_SOCKET_CONNECT_TIMEOUT = 3

# Metrics setting
METRICS_ENABLED = True
RDK_METRICS_DAILY_INRC = "IS:METRICS:"
RDK_METRICS_TYPES_INRC = "IS:METRICS:DATAFOCUS"
RDK_METRICS_HOT_KEYWORDS = "IS:METRICS:KEYWORDS"

# Elasticsearch setting
ELASTICSEARCH_PIPELINE_ENABLED = True
ELASTICSEARCH_SERVER = "10.211.54.227:9300"
ELASTICSEARCH_USERNAME = ""
ELASTICSEARCH_PASSWORD = ""
ELASTICSEARCH_INDEX = "smurfs"
ELASTICSEARCH_TYPE = "items"

# news spider setting
CONFIG_NEWS_FETCH_DEFAULT_DAY = 3
CONFIG_NEWS_BASE_URL = "http://www.toutiao.com"
CONFIG_NEWS_URL_TEMPLATE = "http://www.toutiao.com/api/pc/feed/?category=__all__&utm_source=toutiao&widen=1&max_behot_time=%s&max_behot_time_tmp=%s"
RDK_NEWS_FETCH_TIME = "IS:ROBOT:FETCH"

# news comment spider setting
CONFIG_NEWS_COMMENT_FETCH_NUMBER = 1000
CONFIG_NEWS_COMMENT_BASE_URL = "http://www.toutiao.com"
CONFIG_NEWS_COMMENT_URL = "http://www.toutiao.com/api/comment/list/?group_id=%s&item_id=%s&offset=0"
CONFIG_NEWS_COMMENT_REPLY_URL = "http://www.toutiao.com/api/comment/get_reply/?comment_id=%s&dongtai_id=%s&offset=0&count=%s"

# weibo spider setting
RDK_COOKIE_QUEUE = "IS:ROBOT:%s:COOKIE:%s"

# MySQL setting
MYSQL_PIPELINE_ENABLED = True
MYSQL_SERVER_IP = "localhost"
MYSQL_SERVER_PORT = 3306
MYSQL_CONN_TIMEOUT = 30
MYSQL_SERVER_USER = "root"
MYSQL_SERVER_PASSWORD = "root"
MYSQL_SERVER_DB = "db_weibo"

# HBase setting
HBASE_PIPELINE_ENABLED = True
HBASE_THRIFT_SERVER ="192.168.111.111" #"192.168.11.190"
HBASE_THRIFT_PORT = "9090"

# http download processor setting
PROCESSOR_ENABLED = False
PROCESSOR_RETRY_TIMES = 3
PROCESSOR_RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 408]
PROCESSOR_RETRY_PRIORITY_ADJUST = 1
PROCESSOR_PROXY_ENABLED = False
PROCESSOR_PROXY_USER = "jian.wang04"
PROCESSOR_PROXY_PWD = "82i0v82s"
PROCESSOR_PROXY_SERVER = "http://dps.kuaidaili.com/api/getdps/?orderid=909422589422161&num=50&ut=1&sep=2"
RDK_PROXY_ONE = "IS:ROBOT:PROXY_ONE"
RDK_PROXY_QUEUE = "IS:ROBOT:PROXY_QUEUE"

KAFKA_BROKER_SERVER ="192.168.111.111:9092" #"192.168.11.190:6667"
KAFKA_PUSH_TIMEOUT = 10
KAFKA_TOPIC_NAME = "smurfs"
