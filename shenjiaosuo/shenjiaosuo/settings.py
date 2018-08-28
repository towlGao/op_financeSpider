# -*- coding: utf-8 -*-

# Scrapy settings for shenjiaosuo project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'shenjiaosuo'

SPIDER_MODULES = ['shenjiaosuo.spiders']
NEWSPIDER_MODULE = 'shenjiaosuo.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'shenjiaosuo (+http://www.yourdomain.com)'


# Obey robots.txt rules
ROBOTSTXT_OBEY = False
# LOG_LEVEL = "WARNING"
LOG_LEVEL = "DEBUG"
# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32
USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16
# 超时时间
DOWNLOAD_TIMEOUT = 30
# Disable cookies (enabled by default)
#COOKIES_ENABLED = False
# CONCURRENT_REQUESTS = 20
# CONCURRENT_REQUESTS_PER_DOMAIN = 11

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'shenjiaosuo.middlewares.ShenjiaosuoSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'shenjiaosuo.middlewares.ShenjiaosuoDownloaderMiddleware': 543,
   'shenjiaosuo.middlewares.RandomUserAgentMid': 443,
   'shenjiaosuo.middlewares.ShenjiaosuoRetryMiddleware': 540,
   # 'shenjiaosuo.middlewares.ProxyMid': 440,

}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'shenjiaosuo.pipelines.ShenjiaosuoPipeline': 300,
}

DOWNLOAD_FAIL_ON_DATALOSS = True
# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# 附件存储路径
APPENDIX_DIR = "/data/gaotao/stockex_change/exchange_file/00/"
LOG_SIZE = 10485760
# LOG_SIZE = 10
APP_DIR_SIZE = 150000
UPDATE_FLAG = False
DOWNLOAD_WARNSIZE = 0
# 连接数据库配置
MYSQL_PORT = 3306

# MYSQL_HOST = '140.143.225.98'
MYSQL_HOST = '10.10.0.11'
# MYSQL_USER = 'root'
MYSQL_USER = 'gaotao'
# MYSQL_PASSWD = 'mysql'
MYSQL_PASSWD = '124356'

MYSQL_DATABASE = 'stockexchange'
PROXY_DB = 'callproxy'
EXCHANGE_TABLE_NAME = 'exchange_notice'
COMPANY_TABLE_NAME = 'company_notice'
SHARES_TABLE_NAME = 'shares_list'
NOTICE_UPDATE_NUM = 20
