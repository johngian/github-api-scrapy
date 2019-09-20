BOT_NAME = 'github_api_v3_scraper'

SPIDER_MODULES = ['github_api_v3_scraper.spiders']
NEWSPIDER_MODULE = 'github_api_v3_scraper.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'github_api_v3_scraper.middlewares.HttpAuthenticationPoolMiddleware': 543,
}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'github_api_v3_scraper.pipelines.GithubApiV3ScraperPipeline': 300,
}
