from decouple import config, Csv

BOT_NAME = "github_api_v3_scraper"

SPIDER_MODULES = ["github_api_v3_scraper.spiders"]
NEWSPIDER_MODULE = "github_api_v3_scraper.spiders"

AUTOTHROTTLE_ENABLED = False
AUTOTHROTTLE_TARGET_CONCURRENCY = 3


# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    "github_api_v3_scraper.middlewares.HttpAuthenticationPoolMiddleware": 543
}

# AUTOTHROTTLE_ENABLED = True

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {"github_api_v3_scraper.pipelines.GithubApiV3ScraperPipeline": 300}

# Local settings
GITHUB_REPO_OWNER = config("GITHUB_REPO_OWNER")
GITHUB_REPO_NAME = config("GITHUB_REPO_NAME")
GITHUB_API_TOKENS = config("GITHUB_API_TOKENS", cast=Csv())
DB_PATH = config("DB_PATH")
