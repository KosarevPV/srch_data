import scrapy

from lesson_6.jobs.jobs.items import JobsItem


class SuperjobSpider(scrapy.Spider):
    name = "superjob"
    allowed_domains = ["superjob.ru"]
    start_urls = ["https://www.superjob.ru/vacancy/search/?keywords=python%20developer"]

    @staticmethod
    def get_salary_sj(salary):
        """returns the minimum and maximum salary www.superjob.ru"""

        if salary[0] == 'По договорённости':
            min_salary, max_salary = '-', '-'
        elif salary[0] == 'до':
            min_salary, max_salary = '-', str(salary[-1])
        elif salary[0] == 'от':
            min_salary, max_salary = str(salary[-1]), '-'
        else:
            min_salary = ''.join(salary[0] + salary[-1]).strip()
            max_salary = ''.join(salary[-3] + salary[-1]).strip()
        return min_salary, max_salary

    @staticmethod
    def get_name(post):
        """get a name from a website www.superjob.ru"""
        part_1 = post.xpath(
            ".//span[@class='_1c5Bu _1Yga1 _1QFf5 _2MAQA _1m76X _3UZoC _3zdq9 _1_71a']/a/text()").get()
        part_2 = post.xpath(
            ".//span[@class='_1c5Bu _1Yga1 _1QFf5 _2MAQA _1m76X _3UZoC _3zdq9 _1_71a']/a/span/text()").get()

        if part_2 is None:
            return part_1
        if part_1 is None:
            return 'Не удалось распарсить'
        part_1 = list(map(lambda x: x.strip(), part_1))
        part_2 = list(map(lambda x: x.strip(), part_2))

        if part_1:
            if part_1[0].istitle():
                part_1.append(' ')
                return ''.join(part_1 + part_2)
            part_2.append(' ')
            return ''.join(part_2 + part_1)
        return 'Не удалось распарсить'

    def parse(self, response):
        next_page = response.xpath("//a[@rel='next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        posts = response.xpath("//div[@class='qs65P _39w8W']")
        for i in posts:
            name = self.get_name(i)
            employer = i.xpath(".//div[@class='_3-q4I _3ThDZ X5K3U _3lgWg']/span/a/text()").get()
            employer = employer[0] if employer else 'Не удалось распарсить'
            location = i.xpath(".//div[@class='WDWTW -wsqP T4QPe kcBN3 OzpWI']/div/text()").get()
            min_salary, max_salary = self.get_salary_sj(
                i.xpath(".//span[@class='_2eYAG _1m76X _3UZoC _3zdq9 _3iH_l']/text()").getall())
            href = 'https://www.superjob.ru' + i.xpath(
                ".//span[@class='_1c5Bu _1Yga1 _1QFf5 _2MAQA _1m76X _3UZoC "
                "_3zdq9 _1_71a']/a/@href").get()

            yield JobsItem(
                name=name,
                employer=employer,
                location=location,
                min_salary=min_salary,
                max_salary=max_salary,
                href=href,
            )