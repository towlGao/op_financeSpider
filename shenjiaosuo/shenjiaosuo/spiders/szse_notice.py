# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
import re
import w3lib.url
from hashlib import sha1
from shenjiaosuo.settings import APPENDIX_DIR, NOTICE_UPDATE_NUM
from shenjiaosuo.items import ShenjiaosuoItem
from pprint import pprint
import time

class SzseNoticeSpider(scrapy.Spider):
    '''深交所公告'''
    name = 'szse_notice'
    allowed_domains = ['szse.cn']
    start_urls = ['http://www.szse.cn/disclosure/notice/']

    def parse(self, response):
        item = ShenjiaosuoItem()
        item['l1_title'] = response.xpath(
            "//li[@class='level1 active']/a[not(@href)]/div/text()").extract_first().strip()
        li_list = response.xpath("//li[@class='level1 active']/ul/li")
        for li in li_list:
            l2_url = li.xpath('./a/@href').extract_first()
            item['l2_title'] = li.xpath('.//div/text()').extract_first().strip()
            yield response.follow(
                l2_url,
                meta={'item': deepcopy(item),'flag': 0},
                callback=self.parse_lpage
            )

    def parse_lpage(self, response):
        '''解析列表页'''
        item = response.meta['item']
        flag = response.meta['flag']
        div_list = response.xpath("//div[@class='title']")
        for div in div_list:
            js_data = div.xpath("./script/text()").extract_first()
            item['detail_url'] = re.findall(r"var curHref = '(\./.*?\.[a-zA-Z]{3,4})';", js_data, re.S)[0]
            item['title'] = re.findall(r"var curTitle = '(.*?)';", js_data, re.S)[0]
            item['doc_type_code'] = re.findall(r"var curCmsDocType = '(\d+?)'", js_data)[0]
            item['doc_type'] = item['detail_url'].rsplit(".", 1)[1]
            item['release_time_l'] = div.xpath("./span[@class='time']/text()").extract_first()
            item['release_time_l'] = item['release_time_l'].strip() if item['release_time_l'] else None
            # print(item['doc_type'])

            if item['doc_type'] == 'html':
                # print(item['detail_url'])
                # print(response.url)
                detail_url = response.url.rsplit('/',1)[0]+item['detail_url'][1:]
                item['detail_url'] = detail_url
                yield scrapy.Request(
                    detail_url,
                    callback=self.detail_parse,
                    meta={'item':deepcopy(item)}
                )
                #print("*" * 100)
            else:
                detail_url = response.url.rsplit('/', 1)[0] + item['detail_url'][1:]
                item['detail_url'] = detail_url

                det_url = w3lib.url.canonicalize_url(detail_url)
                s2 = sha1()
                s2.update(det_url.encode())
                fp2 = s2.hexdigest()
                type = detail_url.rsplit('.', 1)[1].lower()
                item['content'] = []
                if type.lower() in ['pdf','doc']:
                    item['content'].append(APPENDIX_DIR + fp2 + '.' + type)
                    # print(item['appendix_path_list'],item['detail_url'],appendix_url)
                    yield scrapy.Request(
                        detail_url,
                        meta={'item': deepcopy(item),'fp1': fp2},
                        callback=self.appendix_parse
                    )
                else:
                    item['content'] = None


        # 翻页
        # time.sleep(0.5)
        flag += 1
        if flag >= NOTICE_UPDATE_NUM:
            return
        current_index = re.findall(r"pageIndex:(\d+),", response.body.decode())[0]
        total_page = re.findall(r"pageCount:(\d+),", response.body.decode())[0]
        current_page = int(current_index)+1
        if current_page<int(total_page):
            next_url = response.url.rsplit("/", 1)[0]+'/index_{}.html'.format(str(current_page))
            #print(next_url)
            yield scrapy.Request(next_url,callback=self.parse_lpage, meta={'item':item,'flag':flag})
        # print("current_page: ",current_page)

    def detail_parse(self,response):
        '''详情页'''
        item = response.meta['item']
        item['title'] = response.xpath('//h2[@class="title"]/text()').extract_first()
        l3_sub_title = response.xpath('//h4[@class="sub-title"]/text()').extract()
        if l3_sub_title:
            item['l3_sub_title'] = l3_sub_title[0]
        else:
            item['l3_sub_title'] = None
        item['release_time'] = response.xpath("//div[@class='des-header']/div[@class='time']/span/text()").extract_first()
        p_list = response.xpath("//div[@id='desContent']//p")
        item['content'] = []
        if p_list:
            for p in p_list:
                p_content = p.xpath(".//text()").extract()
                p_content = [i.strip() for i in p_content]
                item['content'].append(''.join(p_content))

            item['content'] = [j for j in item['content'] if j]
            if item['content']:

                notice_time = item['content'][-1]
                time_list = re.findall(r'(\d+?)年(\d+?)月(\d+?)日', notice_time)
                if time_list:
                    item['notice_time'] = '-'.join(time_list[0])
                    item['content'].pop()
                else:
                    item['notice_time'] = item['release_time']
            else:
                item['content'] = None
        else:
            item['notice_time'] = item['release_time']
            # br_content = response.xpath("//div[@id='desContent']//text()").extract()
            # item['content'] = [con.strip() for con in br_content]
            # item['content'] = [con for con in br_content if con]
            # notice_time = item['content'][-1]
            # notice_time = re.findall(r'(\w+?)年(\w+?)月(\w+?)日',notice_time)
            # if notice_time:
            #     notice_time = list(notice_time[0])
            #     num_map = {'〇': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8,
            #                                 '九': 9, '十': 10}
            #     year = ''.join([num_map[i] for i in notice_time[0]])
            #     month = ''.join([num_map[i] for i in notice_time[1]])
            #     if len(month)>2:
            #         month = month[0]+month[-1]
            #     day = ''.join([num_map[i] for i in notice_time[2]])
            #     if len(day) > 2:
            #         day = day[0] + day[-1]
            #     item['notice_time'] = '-'.join([year,month,day])+'*'*30
            #     item['content'].pop()
            # else:
            #     item['notice_time'] = item['release_time']
        # p_list = response.xpath("//div[@id='desContent']//p")
        # #p_list.pop()
        # p_last = p_list.pop()
        # p_last_con = p_last.xpath(".//text()").extract()
        # p_last_con = [i.strip() for i in p_last_con]
        # p_last_con = [i for i in p_last_con if i]
        # if len(p_last_con)>1:
        #     item['content'].append('$￥'.join(p_last_con))
        # else:
        #     item['content'].append(''.join(p_last_con))
        table_con = response.xpath("//div[@id='desContent']//div[@align='center']//table")
        try:
            if table_con:
                for t in table_con:
                    table_con = t
                table_tr_list = table_con.xpath(".//tr")
                t_c_key = table_tr_list[0]
                td_list = t_c_key.xpath("./td")
                table_key_list = []
                for td in td_list:
                    td_con = td.xpath(".//text()").extract()
                    td_con = [i.strip() for i in td_con]
                    td_con = ''.join(td_con)
                    table_key_list.append(td_con)
                table_value_list = []
                for tr in table_tr_list[1:]:
                    td_list = tr.xpath("./td")
                    tr_value_list = []
                    for td in td_list:
                        td_con = td.xpath(".//text()").extract()
                        td_con = [i.strip() for i in td_con]
                        td_con = ''.join(td_con)
                        tr_value_list.append(td_con)
                    table_value_list.append(tr_value_list)
                table_value_list_2 = []
                for i in range(len(table_key_list)):
                    table_value_list_2.append([v_l[i] for v_l in table_value_list])
                item['table_content'] = dict(zip(table_key_list,table_value_list_2))
            else:
                item['table_content'] = None
        except IndexError as e:
            item['table_content'] = None
        #print(item['table_content'],item['detail_url'])


        # 附件
        appendix_url_list = response.xpath("//div[@id='desContent']//a[contains(@href,'doc') or contains(@href,'DOC' or contains(@href,'pdf') or contains(@href,'PDF'))]/@href").extract()

        if not appendix_url_list:
            item['appendix_path_list'] = None
            # pprint(item)
            yield item
        else:
            # print('附件下载')
            # print('*'*30)
            # print(appendix_url_list)
            item['appendix_path_list'] = []
            for appendix_url in appendix_url_list:
                appendix_url = w3lib.url.canonicalize_url(appendix_url)
                s1 = sha1()
                s1.update(appendix_url.encode())
                fp1 = s1.hexdigest()
                type = appendix_url.rsplit('.',1)[1].lower()
                if type == 'cn':
                    item['appendix_path_list'] = None
                else:
                    item['appendix_path_list'].append(APPENDIX_DIR+fp1+'.'+type)
                    # print(item['appendix_path_list'],item['detail_url'],appendix_url)
                    yield response.follow(
                        appendix_url,
                        meta={'item':deepcopy(item),'fp1':fp1},
                        callback=self.appendix_parse
                    )


    def appendix_parse(self,response):
        '''附件下载'''
        fp1 = response.meta['fp1']
        item = response.meta['item']
        type = response.url.rsplit('.',1)[1].lower()
        with open(APPENDIX_DIR+fp1+'.'+type, 'wb') as f:
            f.write(response.body)
        # pprint(item)
        yield item

