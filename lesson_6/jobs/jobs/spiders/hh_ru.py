import scrapy
from scrapy.http import HtmlResponse

from lesson_6.jobs.jobs.items import JobsItem


class HhRuSpider(scrapy.Spider):
    name = "hh_ru"
    allowed_domains = ["hh.ru"]
    start_urls = ["https://hh.ru/search/vacancy?text=python+developer"]

    @staticmethod
    def get_salary_hh(salary):
        """returns the minimum and maximum salary hh.ru"""
        salary = salary if salary else 0
        if salary == 0:
            min_salary, max_salary = '-', '-'
        elif salary[0] == 'до ':
            min_salary, max_salary = '-', ''.join(salary[1:])
        elif salary[0] == 'от ':
            min_salary, max_salary = ''.join(salary[1:]), '-'
        else:
            money = salary[0].split('–')
            min_salary = ''.join(money[0] + salary[-1]).strip()
            max_salary = ''.join(money[-1] + salary[-1]).strip()
        return min_salary.replace('\u202f', ''), max_salary.replace('\u202f', '')

    def parse(self, response:HtmlResponse):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        posts = response.xpath("//div[@class='vacancy-serp-item-body__main-info']")
        for i in posts:
            name = i.xpath('./div/h3/span/a/text()').get()
            employer = ''.join(i.xpath("./div/div/div/div/div[@class='vacancy-serp-item__meta-info-company']/a/text()").getall())
            location = i.xpath("./div/div/div[@data-qa='vacancy-serp__vacancy-address']/text()").get()
            min_salary, max_salary = self.get_salary_hh(i.xpath("./div/span[@data-qa='vacancy-"
                                                           "serp__vacancy-compensation']/text()").getall())
            href = i.xpath('./div/h3/span/a/@href').get()

            yield JobsItem(
                name=name,
                employer=employer,
                location=location,
                min_salary=min_salary,
                max_salary=max_salary,
                href=href,
            )
