# -*- coding: utf-8 -*-

# Scrapy settings for shangjiaosuo project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'shangjiaosuo'

SPIDER_MODULES = ['shangjiaosuo.spiders']
NEWSPIDER_MODULE = 'shangjiaosuo.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'shangjiaosuo (+http://www.yourdomain.com)'
# LOG_LEVEL = "INFO"
LOG_LEVEL = "DEBUG"
# Obey robots.txt rules
ROBOTSTXT_OBEY = False
USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32
DOWNLOAD_TIMEOUT = 30
# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.005
# CONCURRENT_REQUESTS = 10
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 10
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'shangjiaosuo.middlewares.ShangjiaosuoSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'shangjiaosuo.middlewares.ShangjiaosuoDownloaderMiddleware': 543,
    'shangjiaosuo.middlewares.RandomUserAgentMid': 443,
    'shangjiaosuo.middlewares.ProxyMid': 440,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'shangjiaosuo.pipelines.ShangjiaosuoPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
# 附件存储文件夹路径
APPENDIX_DIR = '/data/gaotao/stockex_change/exchange_file/01/'

# APPENDIX_DIR = "/home/python/Desktop/pdf/"
LOG_SIZE = 10485760
# LOG_SIZE = 10
APP_DIR_SIZE = 150000
# 指为True开启增量，增量每次爬取页数配置NOTICE_UPDATE_NUM
UPDATE_FLAG = False
NOTICE_UPDATE_NUM = 20
# 下载内容（response）大小限制，0表示无限制
DOWNLOAD_WARNSIZE = 0
# 连接数据库配置
MYSQL_PORT = 3306

MYSQL_HOST = '140.143.225.98'
# MYSQL_HOST = '10.10.0.11'
MYSQL_USER = 'root'
# MYSQL_USER = 'gaotao'
MYSQL_PASSWD = 'mysql'
# MYSQL_PASSWD = '124356'

MYSQL_DATABASE = 'stockexchange'
PROXY_DB = 'callproxy'
EXCHANGE_TABLE_NAME = 'exchange_notice'
COMPANY_TABLE_NAME = 'company_notice'
SHARES_TABLE_NAME = 'shares_list'

