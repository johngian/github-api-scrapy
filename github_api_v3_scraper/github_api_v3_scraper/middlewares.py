import random


class HttpAuthenticationPoolMiddleware(object):
    def __init__(self, tokens):
        self.tokens = tokens

    @classmethod
    def from_crawler(cls, crawler):
        tokens = crawler.settings.getlist("GITHUB_API_TOKENS")

        # instantiate the extension object
        ext = cls(tokens)

        return ext

    def process_request(self, request, spider):
        token = random.choice(self.tokens)
        request.headers["Authorization"] = token
