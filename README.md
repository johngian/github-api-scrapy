# github-api-scrapy
Use scrapy to consume GitHub API

Instructions:

```
> pip install -r requirements.txt
> cd src/
> scrapy runspider github_api_v3_scraper/spiders/issues.py \
    -o <output_path> -s "GITHUB_REPO_OWNER=<owner>"
    -s "GITHUB_REPO_NAME=<name>"
    -s "GITHUB_API_TOKENS=<COMMA_SEPERATED_AUTH_TOKENS>"
```
