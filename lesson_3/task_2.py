from pymongo import MongoClient


def convert_money(s):
    if '-' != s:
        s = s.split()
        if s[-1] == 'USD':
            s = int(''.join(s[:-1])) * 82
        elif s[-1] == 'EUR':
            s = int(''.join(s[:-1])) * 89
        elif s[-2] == 'бел.':
            s = int(''.join(s[:-2])) * 28
        else:
            s = int(''.join(s[:-1]))
    else:
        s = 0
    return s


def gt_filter(max_salary):
    client = MongoClient()
    db = client.vacancys_db
    data = []
    for i in db.vacancys.find():
        min_s = convert_money(i['min_salary'])
        max_s = convert_money(i['max_salary'])
        if min_s >= max_salary or max_s >= max_salary:
            data.append(i)

    return data


def main():
    max_salary = int(input('Введите минимальную для вас заработную плату: '))
    data_list = gt_filter(max_salary)

    for i in data_list:
        print(i)


if __name__ == '__main__':
    main()
