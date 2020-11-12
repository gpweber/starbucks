# File contains Scrapy settings for the Starbucks Project

BOT_NAME = 'starbucks'

SPIDER_MODULES = ['starbucks.spiders']
NEWSPIDER_MODULE = 'starbucks.spiders'

USER_AGENT="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
# Crawl responsibly by identifying yourself (and your website) on the user-agent


ROBOTSTXT_OBEY = False
# Obey robots.txt rules

DOWNLOAD_DELAY = 1.5

ITEM_PIPELINES = {
    'starbucks.pipelines.WriteItemPipeline': 300
}
# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
