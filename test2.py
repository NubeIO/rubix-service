import requests

r = requests.get('https://api.github.com/repos/NubeDev/bacnet-flask/releases')
status = r.status_code
r = r.json()

user_selected = "https://api.github.com/repos/NubeDev/bacnet-flask/zipball/v1.1.1"

if status == 200:
    for item in r:
        print(item)

# print(r.json())

# for v, k in r.items():
#     if not isinstance(k, list):
#         for x, y in k.items():
#             print(x,':', y)
