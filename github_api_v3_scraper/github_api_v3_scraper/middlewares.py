from scrapy.downloadermiddlewares import DownloaderMiddleware


class HttpAuthenticationPoolMiddleware(DownloaderMiddleware):
    def process_request(self, request, spider):
        tokens = spider.settings.getlist("GITHUB_API_TOKENS")
        token = random.choice(tokens)
        request.headers["Authorization"] = token
        return request
