from scrapy.cmdline import execute
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


# 列表页
execute(['scrapy', 'crawl', 'JDDJ_url'])
# 详情
# execute(['scrapy', 'crawl', 'JDDJ_Detail'])