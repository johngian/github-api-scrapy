import json

from scrapy import Spider
from scrapy.http import Request

from github_api_v3_scraper.utils import get_next


class IssueSpider(Spider):
    """Scrape github issues list from Github API"""

    name = "issues"
    allowed_domains = ["api.github.com"]

    def start_requests(self):
        url = "https://api.github.com/repos/{owner}/{repo}/issues".format(
            owner=self.settings.get("GITHUB_REPO_OWNER"),
            repo=self.settings.get("GITHUB_REPO_NAME"),
        )
        yield Request(url, callback=self.parse_issues)

    def parse_events(self, response):
        data = {"events": json.loads(response.text), "issue": response.meta["issue"]}
        yield data

    def parse_issue(self, response):
        data = json.loads(response.text)
        events_url = data["events_url"]
        yield Request(events_url, callback=self.parse_events, meta={"issue": data})

    def parse_issues(self, response):
        data = json.loads(response.text)
        for issue in data:
            yield Request(issue["url"], callback=self.parse_issue)

        if self.get_next(response.headers):
            yield response.follow(l, callback=self.parse)
