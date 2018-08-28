#!/bin/bash
#cd /home/gaotao/myspider/shangjiaosuo
cd /home/python/Desktop/myspider/shangjiaosuo
#workon gt_spider

scrapy crawl sse_cp_notice -s JOBDIR=job_info/003 >> sse_cp_notice.log 2>&1 &
