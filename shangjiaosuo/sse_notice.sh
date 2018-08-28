#!/bin/bash
cd /home/gaotao/myspider/shangjiaosuo
#workon gt_spider

scrapy crawl sse_notice >> sse_notice.log 2>&1 &
