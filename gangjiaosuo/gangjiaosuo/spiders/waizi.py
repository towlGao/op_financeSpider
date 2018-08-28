# -*- coding: utf-8 -*-
import scrapy


class WaiziSpider(scrapy.Spider):
    name = 'waizi'
    allowed_domains = ['hkexnews.hk']
    start_urls = ['http://waizi.com/']

    def parse(self, response):
        pass
