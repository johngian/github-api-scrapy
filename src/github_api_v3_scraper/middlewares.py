import logging
import random
import time

from twisted.internet import reactor, defer


class HttpAuthenticationPoolMiddleware(object):
    def __init__(self, tokens):
        self.tokens = tokens

    @classmethod
    def from_crawler(cls, crawler):
        tokens = crawler.settings.get("GITHUB_API_TOKENS")

        # instantiate the extension object
        ext = cls(tokens)

        return ext

    def process_request(self, request, **kwargs):
        token = random.choice(self.tokens)
        auth = "token {}".format(token)
        request.headers["Authorization"] = auth


class RetryGithubRateLimitMiddleware(object):
    def process_response(self, request, response, **kwargs):
        header = "X-RateLimit-Reset"
        if response.status == 403 and header in response.headers:
            reset = int(response.headers.get("X-RateLimit-Reset"))
            now = int(time.time())
            delay = (reset - now) + 10 * 60

            d = defer.Deferred()
            reactor.callLater(delay, d.callback, None)

            logger = logging.getLogger()
            logger.warning("Delayed retry for request: {}".format(request))

            return d
        return response
