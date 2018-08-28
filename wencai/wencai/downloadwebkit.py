# -*- coding: utf-8 -*-
# -*- create by gt 18-8-16 -*-
# import spynner
# import pyquery
import time
import sys
from scrapy.http import HtmlResponse


#
# class WebkitDownloaderTest(object):
#     def process_request(self, request, spider):
#         #        if spider.name in settings.WEBKIT_DOWNLOADER:
#         #            if( type(request) is not FormRequest ):
#         browser = spynner.Browser()
#         browser.create_webview()
#         browser.set_html_parser(pyquery.PyQuery)
#         browser.load(request.url, 20)
#         try:
#             browser.wait_load(10)
#         except:
#             pass
#         string = browser.html
#         string = string.encode('utf-8')
#         renderedBody = str(string)
#         return HtmlResponse(request.url, body=renderedBody)
#

from selenium.common.exceptions import TimeoutException
import time

class SeleniumMiddleware(object):
    def process_request(self, request, spider):
        try:
            spider.browser.get(request.url)

        except TimeoutException as e:
            print('超时')
            page_source = spider.browser.page_source
        time.sleep(2)
        return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source,
                            encoding="utf-8", request=request)

