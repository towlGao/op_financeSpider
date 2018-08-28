# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy



class ShenjiaosuoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    l1_title = scrapy.Field()
    l2_title = scrapy.Field()
    title = scrapy.Field()
    detail_url = scrapy.Field()
    doc_type_code = scrapy.Field()
    doc_type = scrapy.Field()
    content = scrapy.Field()
    l3_sub_title = scrapy.Field()
    release_time = scrapy.Field()
    notice_time = scrapy.Field()
    table_content = scrapy.Field()
    appendix_path_list = scrapy.Field()
    release_time_l = scrapy.Field()

    # appendix_path_list = scrapy.Field()
    # appendix_path_list = scrapy.Field()
    # appendix_path_list = scrapy.Field()


class ShenjiaosuoItemCp(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    l1_title = scrapy.Field()
    l2_title = scrapy.Field()
    title = scrapy.Field()
    detail_url = scrapy.Field()
    category = scrapy.Field()
    doc_type = scrapy.Field()
    content = scrapy.Field()
    sec_code = scrapy.Field()
    sec_name = scrapy.Field()
    publish_time = scrapy.Field()
    # notice_time = scrapy.Field()
    # table_content = scrapy.Field()
    appendix_path = scrapy.Field()
    handle_time = scrapy.Field()
    # release_time = scrapy.Field()
    # appendix_path_list = scrapy.Field()
    # appendix_path_list = scrapy.Field()
    # appendix_path_list = scrapy.Field()
