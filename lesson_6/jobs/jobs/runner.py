from twisted.internet import reactor

from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from spiders.hh_ru import HhRuSpider
from spiders.superjob import SuperjobSpider


if __name__ == '__main__':
    configure_logging()
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    runner.crawl(SuperjobSpider)
    runner.crawl(HhRuSpider)
    reactor.run()
