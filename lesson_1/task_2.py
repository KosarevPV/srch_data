import json
from time import sleep

import requests

from key import key

access_token = key
req = requests.get(f'https://api.vk.com/method/groups.get?&v=5.81&access_token={access_token}')
data = req.json()
with open('vk.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

for k in data['response']['items']:
    group_req = requests.get(f'https://api.vk.com/method/groups.getById?&v=5.81&group_ids={k}&access_token={access_token}')
    try:
        print(group_req.json()['response'][0]['name'])
    except KeyError:
        sleep(2)
        group_req = requests.get(
            f'https://api.vk.com/method/groups.getById?&v=5.81&group_ids={k}&access_token={access_token}')
        print(group_req.json()['response'][0]['name'])
