import os
import scrapy
from dotenv import load_dotenv


class GbSpider(scrapy.Spider):
    load_dotenv()
    email = os.getenv('LOGIN')
    password = os.getenv('PASSWORD')
    csrf = os.getenv('CSRF')
    name = "gb"
    url = "https://gb.ru/login"

    allowed_domains = ["gb.ru"]
    start_urls = ["https://gb.ru/login"]

    def parse(self, response):
        yield scrapy.FormRequest(
            self.url,
            method="POST",
            callback=self.login,
            formdata={'user_email': self.email, 'user_password': self.password},
            headers={'csrf-token': self.csrf}
        )

    def login(self, response):
        print(response.text)
        pass
