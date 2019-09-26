import logging
import random
import time

from twisted.internet import reactor, defer

from peewee import CharField, Model
from playhouse.sqlite_ext import IntegerField, SqliteExtDatabase


logger = logging.getLogger()


class RateLimit(Model):
    token = CharField()
    remaining = IntegerField()


class HttpAuthenticationPoolMiddleware(object):
    def __init__(self, tokens, db_path):
        self.tokens = tokens
        db = SqliteExtDatabase(db_path)
        db.bind([RateLimit])
        db.connect()
        db.create_tables([RateLimit])

    def _get_token(self):
        query = RateLimit.select().order_by(RateLimit.remaining.desc())
        available_tokens = self.tokens

        if query.count() > 0:
            if query.count() >= len(self.tokens):
                return query[0].token
            else:
                query_tokens = [e.token for e in query]
                available_tokens = [t for t in self.tokens if t not in query_tokens]

        return random.choice(available_tokens)

    @classmethod
    def from_crawler(cls, crawler):
        tokens = crawler.settings.get("GITHUB_API_TOKENS")
        db_path = crawler.settings.get("DB_PATH")

        # instantiate the extension object
        ext = cls(tokens, db_path)

        return ext

    def process_request(self, request, **kwargs):
        token = self._get_token()
        auth = "token {}".format(token)
        request.headers["Authorization"] = auth

    def _retry(self, request, delay):
        d = defer.Deferred()
        req = request.copy()
        reactor.callLater(delay, d.callback, request)
        return d

    def process_response(self, request, response, **kwargs):

        # Store remaining API calls per token
        remaining_header = "X-RateLimit-Remaining"
        if remaining_header in response.headers:
            remaining = int(response.headers[remaining_header])
            token = request.headers["Authorization"].lstrip(b"token ")

            if RateLimit.select().where(RateLimit.token == token):
                RateLimit.update(remaining=remaining).where(RateLimit.token == token)
            else:
                RateLimit.create(token=token, remaining=remaining)

        # Defer calls if throttled
        if response.status == 403:

            reset_header = "X-RateLimit-Reset"
            if reset_header in response.headers:
                reset = int(response.headers.get(reset_header))
                now = int(time.time())
                delay = (reset - now) + 10 * 60

                logger.warning(
                    "Delayed retry for request: {}. Reason: 'RateLimit'".format(request)
                )
                return self._retry(request, delay)

            retry_header = "Retry-After"
            if retry_header in response.headers:
                delay = 3 * int(response.headers["Retry-After"])

                logger.warning(
                    "Delayed retry for request: {}. Reason 'Retry-After'".format(
                        request
                    )
                )
                return self._retry(request, delay)

        return response
