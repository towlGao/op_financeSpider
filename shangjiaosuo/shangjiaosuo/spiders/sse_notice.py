# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
import re
import w3lib.url
from hashlib import sha1
from shangjiaosuo.settings import APPENDIX_DIR


class SseNoticeSpider(scrapy.Spider):
    name = 'sse_notice'
    allowed_domains = ['sse.com.cn']
    start_urls = ['http://www.sse.com.cn/disclosure/announcement/general/','http://www.sse.com.cn/disclosure/announcement/listing/']

    def parse(self, response):
        '''列表页'''
        dd_list = response.xpath("//div[@id='sse_list_1']/dl/dd")
        if not dd_list:
            return
        for dd in dd_list:
            item = {}
            if re.findall(r'http://www.sse.com.cn/disclosure/announcement/general/', response.url):
                item['l2_title'] = '一般公告'
            if re.findall(r'http://www.sse.com.cn/disclosure/announcement/listing/', response.url):
                item['l2_title'] = '上市/退市公告'
            item['release_time'] = dd.xpath("./span/text()").extract_first()
            item['detail_url'] = dd.xpath("./a/@href").extract_first()
            item['detail_url'] = response.url.rsplit("/", 4)[0] + item['detail_url']
            item['title'] = dd.xpath("./a/@title").extract_first()
            yield scrapy.Request(
                item['detail_url'],
                meta={'item': deepcopy(item)},
                callback=self.detail_parse
            )
        ret = re.findall(r's_index_(\d+)\.htm', response.url.rsplit("/", 1)[1])
        ret = ret[0] if ret else 1
        # 增量式
        current_page = ret
        if current_page >5:
            return
        next_url = response.url.rsplit("/", 1)[0] + '/s_index_{}.htm'.format(str(int(ret) + 1))
        yield scrapy.Request(
            next_url,
            method='POST',
            callback=self.parse
        )

    def detail_parse(self, response):
        '''详情页'''
        item = response.meta['item']
        p_list = response.xpath("//div[@class='allZoom']/p")
        item['content'] = []
        if not p_list:
            p_list = response.xpath("//div[@class='article-infor']/p")
        for p in p_list:
            c_list = p.xpath(".//text()").extract()
            p_con = ''.join([c.strip() for c in c_list])
            p_con = re.sub(r'\xa0', '', p_con)
            if p_con:
                item['content'].append(p_con)
        item['content'] = [con.strip() for con in item['content'] if con.strip()]
        sub_title = item['content'][0]
        ret = re.match(r'上证.{,23}号',sub_title)
        if ret:
            item['content'].pop(0)
        notice_time = item['content'][-1]
        n_time = re.findall(r'(\w{2,4})年(\w+?)月(\w+?)日', notice_time)
        if n_time:
            item['content'].pop()
            # print('*'*100)
        n_time = '-'.join(n_time[0]) if n_time else item['release_time']
        for i in ['特此公告。', '上海证券交易所', '上海证券交易所                  深圳证券交易所', '特此通知。']:
            if i in item['content']:
                item['content'].remove(i)
        item['notice_time'] = n_time

        notice_time_list = re.findall(r'\d+', item['notice_time'])
        item['notice_time'] = item['notice_time'] if notice_time_list else item['release_time']
        appendix_url_list = response.xpath("//div[@class='allZoom']//a/@href").extract()
        item['appendix_list'] = []
        # item['appendix_type'] = []
        if appendix_url_list:
            flag = [0,0]
            for appendix_url in appendix_url_list:
                doc_type = appendix_url.rsplit('.', 1)[1]
                # item['appendix_type'].append(doc_type)
                if doc_type.lower() in ['shtml','htm', 'html', 'cn', 'com']:
                    flag[0] = 1
                else:
                    flag[1] = 1
                    yield response.follow(appendix_url,
                                          meta={'item': deepcopy(item), 'type': doc_type},
                                          callback=self.appendix_parse
                                          )
            if flag[0] == 1 and flag[1] != 1:
                yield item
                # print(item)
        else:
            yield item
            # print(item)

    def appendix_parse(self, response):
        '''附件'''
        item = response.meta['item']
        type = response.meta['type']
        url = response.url
        appendix_url = w3lib.url.canonicalize_url(url)
        s1 = sha1()
        s1.update(appendix_url.encode())
        fp1 = s1.hexdigest()
        with open(APPENDIX_DIR + fp1 + '.' + type, 'wb') as f:
            f.write(response.body)
        item['appendix_list'].append(APPENDIX_DIR + fp1 + '.' + type)
        yield item
        # print(item)
