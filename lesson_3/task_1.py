from time import sleep

import requests
from lxml import html
from pymongo import MongoClient


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
    return min_salary, max_salary


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


def scarp_hh(params, headers, max_pages, data_list):
    """Scarp hh.ru"""

    url = 'https://hh.ru/search/vacancy'
    source = url.split('/')[2]

    while True:
        if params['page'] >= max_pages:
            break

        response = requests.get(url, headers=headers, params=params)
        dom = html.fromstring(response.text)
        posts = dom.xpath("//div[@class='vacancy-serp-item-body__main-info']")
        if len(posts) == 0:
            break
        for i in posts:
            name = i.xpath('./div/h3/span/a/text()')[0]
            employer = ''.join(i.xpath("./div/div/div/div/div[@class='vacancy-serp-"
                                       "item__meta-info-company']/a/text()"))
            location = i.xpath("./div/div/div[@data-qa='vacancy-serp__vacancy-address']/text()")[0]
            min_salary, max_salary = get_salary_hh(i.xpath("./div/span[@data-qa='vacancy-"
                                                           "serp__vacancy-compensation']/text()"))
            href = i.xpath('./div/h3/span/a/@href')[0]

            data_dict = {
                "name": name,
                "employer": employer,
                "location": location,
                "min_salary": min_salary,
                "max_salary": max_salary,
                "href": href,
                "source": source,
            }
            data_list.append(data_dict)
        params['page'] += 1
        sleep(0.5)


def get_name(post):
    """get a name from a website www.superjob.ru"""
    part_1 = post.xpath(
        ".//span[@class='_1c5Bu _1Yga1 _1QFf5 _2MAQA _1m76X _3UZoC _3zdq9 _1_71a']/a/text()")
    part_2 = post.xpath(
        ".//span[@class='_1c5Bu _1Yga1 _1QFf5 _2MAQA _1m76X _3UZoC _3zdq9 _1_71a']/a/span/text()")
    part_1 = list(map(lambda x: x.strip(), part_1))
    part_2 = list(map(lambda x: x.strip(), part_2))
    if part_1:
        if part_1[0].istitle():
            return ' '.join(part_1 + part_2)
        return ' '.join(part_2 + part_1)
    return 'Не удалось распарсить'


def scarp_superjob(params, headers, max_pages, data_list):
    """Scarp www.superjob.ru"""

    url = 'https://www.superjob.ru/vacancy/search/'
    source = url.split('/')[2]

    while True:
        if params['page'] >= max_pages + 1:
            break

        response = requests.get(url, headers=headers, params=params)
        dom = html.fromstring(response.text)
        posts = dom.xpath("//div[@class='qs65P _39w8W']")
        if len(posts) == 0:
            break
        for i in posts:
            name = get_name(i)
            employer = i.xpath(".//div[@class='_3-q4I _3ThDZ X5K3U _3lgWg']/span/a/text()")
            employer = employer[0] if employer else 'Не удалось распарсить'
            location = i.xpath(".//div[@class='WDWTW -wsqP T4QPe kcBN3 OzpWI']/div/text()")[0]
            min_salary, max_salary = get_salary_sj(
                i.xpath(".//span[@class='_2eYAG _1m76X _3UZoC _3zdq9 _3iH_l']/text()"))
            href = source + i.xpath(
                ".//span[@class='_1c5Bu _1Yga1 _1QFf5 _2MAQA _1m76X _3UZoC "
                "_3zdq9 _1_71a']/a/@href")[0]

            data_dict = {
                "name": name,
                "employer": employer,
                "location": location,
                "min_salary": min_salary,
                "max_salary": max_salary,
                "href": href,
                "source": source,
            }
            data_list.append(data_dict)

        params['page'] += 1
        sleep(0.5)


def main():
    """main func"""
    post = input('Введите желаемую должность: ')
    pages = input('Сколько страниц просмотреть (оставьте пустым если хотите просмотреть все): ')

    max_pages = int(pages) if pages.isdigit() else float('inf')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 /'
                      '(KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    }

    hh_params = {
        'text': post,
        'page': 0,
        'area': 1002,
    }

    superjob_params = {
        'keywords': post,
        'page': 1,
    }

    data_list = []

    scarp_hh(hh_params, headers, max_pages, data_list)
    scarp_superjob(superjob_params, headers, max_pages, data_list)

    client = MongoClient()
    db = client.vacancys_db

    print(f'Записей в таблице {db.vacancys.count_documents({})} до выполнения скрипта')
    total = 0
    new = 0
    for i in data_list:
        vacancy_in_db = db.vacancys.find(
            {
                'name': i['name'],
                'employer': i['employer'],
                'location': i['location'],
                'min_salary': i['min_salary'],
                'max_salary': i['max_salary'],
            }
        )

        if not list(vacancy_in_db):
            db.vacancys.insert_one(i)
            new += 1
        total += 1

    print(f'Из {total} просмотренных вакансий {new} новых')
    print(f'Записей в таблице {db.vacancys.count_documents({})} после выполнения скрипта')


if __name__ == '__main__':
    main()
