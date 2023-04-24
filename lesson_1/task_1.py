import json

import requests


req = requests.get('https://api.github.com/users/KosarevPV/repos')
data = req.json()
with open('git_hub.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4, ensure_ascii=False)


for k in data:
    print(k['name'])
