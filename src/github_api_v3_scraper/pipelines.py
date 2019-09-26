import logging

from peewee import Model
from playhouse.sqlite_ext import JSONField, SqliteExtDatabase


class Issue(Model):
    item = JSONField()


class GithubApiV3ScraperPipeline(object):
    def __init__(self, db_path):
        db = SqliteExtDatabase(db_path)
        db.bind([Issue])
        db.connect()
        db.create_tables([Issue])

    @classmethod
    def from_crawler(cls, crawler):
        db_path = crawler.settings.get("DB_PATH")
        return cls(db_path)

    def process_item(self, item, spider):
        issue = Issue(item={"issue": item["issue"], "events": item["events"]})
        issue.save()

        logger = logging.getLogger()
        logger.info("Added item to DB: {}".format(item["issue"]["number"]))

        return item
